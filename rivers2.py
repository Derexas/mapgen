import numpy as np
import random

TOP = 1; BOTTOM = 0; RIGHT = 2; LEFT = 3; END = 8;
FLOWDIRECTIONS = [[1,0],[-1,0],[0,1],[0,-1],[-1,-1],[-1,1],[1,1],[1,-1]]
OCEANLEVEL = 0.2; OCEANDRAIN = -50; ZERO = 0.004

def fillDrain(heightmap,drainsmap,drains,flowheatmap,di,exitss,
		volumes,H,lakes,rivers,ignore):
	if di in ignore:
		return
	drain = drains[di]
	ye,xe = drain[0][1]
	drain.sort()
	s = 0
	drainid = di+2 #begins at 2
	exits = exitss[di]
	for i,(h,(y,x),filled) in enumerate(drain):
		if filled:
			continue #reloop to next
		lakes[di].append((h,(y,x)))
		drain[i] = (h,(y,x),True)
		for yt,xt in [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]: #test overflow
			if drainsmap[yt][xt] != drainid:
				exits.append((heightmap[yt][xt],(yt,xt)))
				exits.sort() #put the lowest exit first
		if len(exits) > 0 and exits[0][0] <= h: #overflow				
			ye,xe = exits[0][1] #exit position
			flowedzoneid = drainsmap[ye][xe] #new flowing zone
			fdi = flowedzoneid-2
			if flowedzoneid == 1: #to the ocean
				#print("flow into ocean at", (ye, xe))
				rivers.append((ye,xe))
				volumes[di] = 0 #set remaining volume for this zone to 0
			elif H[di] > H[fdi] and H[di] - H[fdi] < 0.001: #same level (== prob not correct)
				#need to fuse and run algo on fused zone
				volumes[di] += volumes[fdi]
				for hf,(yf,xf),f in drains[fdi]:
					drainsmap[yf][xf] = drainid #fuse drainmaps
				for hl,(yl,xl) in lakes[fdi]:
					lakes[di].append((hl,(yl,xl)))
				lakes[fdi] = []
				drains[di] += drains[fdi]
				print(len(drains[di]))
				exitss[di] += exitss[fdi]
				nexits = []
				for hne,(yne,xne) in exitss[di]:
					if (drainsmap[yne][xne] != drainid and
							drainsmap[yne][xne] != flowedzoneid):
						nexits.append((hne,(yne,xne)))
				exitss[di] = nexits
				ignore.append(fdi) #for when the fdi lake has not been made already 
				print("level/fuse", drainid, "with", flowedzoneid, "at", (ye, xe), exits[0], H[di],H[fdi])
				fillDrain(heightmap,drainsmap,drains,flowheatmap,
					di,exitss,volumes,H,lakes,rivers,ignore)
				return
			elif H[di] > H[fdi]: #lower level: flow into
				volumes[fdi] += volumes[di]
				volumes[di] = 0 #set remaining volume for this zone to 0
				#print("flow into", flowedzoneid, "at", (ye, xe), exits[0])
				fillDrain(heightmap,drainsmap,drains,flowheatmap,
					fdi,exitss,volumes,H,lakes,rivers,ignore)
				if di in ignore: #filled drain has level and removed current drain
					return
				else: #a river goes into the filled drain
					rivers.append((ye,xe))
			else: #higher level: continue to fill itself
				pass
		hdif = drain[i+1][0] - h #prob is zone not big enough (too much flow for the minima sizes)
		H[di] += hdif
		s += 1
		volumes[di] -= s * hdif
		if volumes[di] <= 0:
			H[di] -= -volumes[di]/s
			break
		lakes[di][0] = (H[di],lakes[di][0][1])
	#rc = random.choice(lake)
	#print(rc, heightmap[rc[1][0]][rc[1][1]])
	#lakes.append(lake)
	#print((ye,xe), volumes[di], s, H[di])

def lakesMap(heightmap,drainsmap,drains,flowheatmap,flowmap):
	lakes, rivers = [], []
	volumes, drainids, H, exitss = [], [], [], []
	for drain in drains:
		for i,(h,(x,y)) in enumerate(drain):
			drain[i] = (h,(x,y),False)
		ye,xe = drain[0][1]
		surface = flowheatmap[ye][xe]
		volume = surface*1000
		volumes.append(volume)
		H.append(drain[0][0]) #lake height begins at lowest point
		exitss.append([])
		lakes.append([])
	ignore = [] #drains to be ignored
	for di,drain in enumerate(drains):
		fillDrain(heightmap,drainsmap,drains,
			flowheatmap,di,exitss,volumes,H,lakes,rivers,ignore)
	height, width = len(heightmap), len(heightmap[0])
	lakesmap = [[0]*width for _ in range(height)]
	waterhmap = [[0]*width for _ in range(height)]
	lakeid = 1
	for lake in lakes:
		for h,(y,x) in lake:
			waterhmap[y][x] = lake[0][0]
			lakesmap[y][x] = lakeid
		lakeid += 1
	riverid = lakeid
	print(len(rivers), "rivers")
	for yr,xr in rivers:
		while lakesmap[yr][xr] == 0 and drainsmap[yr][xr] != 0 and flowmap[yr][xr] != END:
			lakesmap[yr][xr] = riverid
			heightmap[yr][xr] -= 0.001
			yd, xd = FLOWDIRECTIONS[flowmap[yr][xr]]
			yr += yd
			xr += xd
	oceanid = riverid+10
	# for y,x in np.ndindex((height,width)):
	# 	if drainsmap[y][x] == 0:
	# 		lakesmap[y][x] = oceanid
	return lakesmap,waterhmap


def flowHeatMap(flowmap):
	height, width = len(flowmap), len(flowmap[0])
	flowheatmap = [[0]*width for _ in range(height)]
	for y,x in np.ndindex((height,width)):
		while flowmap[y][x] != -1 and flowmap[y][x] != END:
			yxd = FLOWDIRECTIONS[flowmap[y][x]]
			y += yxd[0]
			x += yxd[1]
			flowheatmap[y][x] += 1
	return flowheatmap

def flowMap(heightmap):
	height, width = len(heightmap), len(heightmap[0])
	flowmap = [[[None]*width for _ in range(height)] for __ in range(3)]
	flowgraph = []
	for y,x in np.ndindex((height,width)):
		if heightmap[y][x] > OCEANLEVEL:
			h = heightmap[y][x]
			d = []
			for D in FLOWDIRECTIONS:
				d.append(heightmap[y+D[0]][x+D[1]] - h)
			sqrt2 = 2**0.5
			for i in range(3,8): #divide by hori/diago ratio
				d[i] /= sqrt2
			steepest = d.index(min(d))
			if d[steepest] < 0:
				flowmap[0][y][x] = steepest
				# D = FLOWDIRECTIONS[steepest]
				# flowmap[2][y][x] = (d[steepest], (y+D[0], x+D[1]))
			else:
				flowmap[0][y][x] = END
			if abs(d[steepest]) < ZERO:
				d[steepest] = 0
			flowmap[1][y][x] = d[steepest]
		else:
			flowmap[0][y][x] = -1
			flowmap[1][y][x] = -1
	return flowmap

def drainageBasins(heightmap,flowmap):
	drainid = 2;
	height, width = len(heightmap), len(heightmap[0])	
	drainmap = [[0]*width for _ in range(height)]
	drains = []
	ends = []
	nends = 0
	for y,x in np.ndindex((height,width)):
		path = []
		while flowmap[0][y][x] != -1 and flowmap[0][y][x] != END and drainmap[y][x] == 0:
			direction = flowmap[0][y][x]
			path.append((y,x))
			y += FLOWDIRECTIONS[direction][0] #follow the flow
			x += FLOWDIRECTIONS[direction][1]
		if drainmap[y][x] == 0: #unexplored tile
			if flowmap[0][y][x] == END: #new minima
				nends += 1
				di = drainid
				for ye,xe in ends:
					if abs(ye-y) <= 1 and abs(xe-x) <= 1:
						di = drainmap[ye][xe] #fuse with close drain
						nends -= 1
						break
				if di == drainid: #new drain
					drainid += 1
					drains.append([])
				drainmap[y][x] = di
				drains[di-2].append(((heightmap[y][x]),(y,x)))
				ends.append((y,x))
			elif flowmap[0][y][x] == -1: #sea
				di = 1
			else:
				di = -100
		else: #already assigned minima
			di = drainmap[y][x]
			if di != 1:
				drains[di-2].append(((heightmap[y][x]),(y,x)))
		for yf,xf in path: #set the id of the path
			drainmap[yf][xf] = di
			if di != 1:
				drains[di-2].append((heightmap[yf][xf],(yf,xf)))
	print(len(ends), nends, "ends")
	for ye,xe in ends:
		pass
		#drainmap[ye][xe] = 0
	print(drains[0][0:1])
	return drainmap,drains

def exploreFlat(basinsmap, flowmap, yi, xi, bid):
	pile = []
	pile.append((yi,xi))
	while len(pile) > 0:
		y, x = pile.pop()
		if basinsmap[y][x] == 0 and abs(flowmap[1][y][x]) < ZERO and flowmap[0][y][x] != 0:
			basinsmap[y][x] = bid
			pile.append((y+1, x))
			pile.append((y-1, x))
			pile.append((y, x+1))
			pile.append((y, x-1))

def flatMap(flowmap):
	height, width = len(flowmap[0]), len(flowmap[0][0])
	basinsmap = [[0]*width for _ in range(height)]
	bid = 1
	for y,x in np.ndindex((height,width)):
		if flowmap[0][y][x] != 0: #not ocean
			exploreFlat(basinsmap, flowmap, y, x, bid)
			if basinsmap[y][x] == bid: #used the id
				bid += 1
	return basinsmap