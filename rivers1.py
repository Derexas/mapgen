TOP = 0; BOTTOM = 1; RIGHT = 2; LEFT = 3; END = 4; UNKNOW = 5; SOURCE = 6
FLOWDIRECTIONS = [[1,0],[-1,0],[0,1],[0,-1]]


def flow(source, flowMap, flowWeightMap, depthMap):
	flows = []
	willFlow = [source]
	while len(willFlow) > 0:
		print(str(len(willFlow)) + " flowing")
		flowing = willFlow
		willFlow = []
		for s in flowing:
			i = 0
			RFD = list(FLOWDIRECTIONS)
			random.shuffle(RFD)
			for direction in RFD:
				# fucked up condition to get proper i
				i = max(0, 2*direction[1]-direction[0]) if direction[1] != -1 else 3
				# (-) : opposite of flow
				y, x = s['y'] - direction[0], s['x'] - direction[1]
				newWeight = s['weight'] + max(0, depthMap[y][x]-depthMap[s['y']][s['x']])
				if flowMap[y][x] == UNKNOW:
					willFlow.append({'y': y, 'x': x, 'weight': newWeight})
					flowWeightMap[y][x] = newWeight
					flowMap[y][x] = i
				elif flowWeightMap[y][x] > newWeight:
					dif = flowWeightMap[y][x] - newWeight
					flowWeightMap[y][x] = newWeight
					ytmp, xtmp = y, x
					"""while flowMap[ytmp][xtmp] <= 3:
						print(flowMap[ytmp][xtmp], ytmp, xtmp)
						dir = FLOWDIRECTIONS[flowMap[ytmp][xtmp]]
						ytmp, xtmp = ytmp - dir[0], xtmp - dir[1]
						flowWeightMap[ytmp][xtmp] -= dif"""
					flowMap[y][x] = i

				#i += 1


def rivers(flowMap, flowWeightMap, depthMap, moistureMap, biomeMap, sourceHeight):
	sources = []
	# init
	for y in range(height):
		flowMap.append([])
		flowWeightMap.append([])
		for x in range(width):
			flowMap[y].append(UNKNOW)
			flowWeightMap[y].append(0)
			if y == height-1 or x == width-1 or biomeMap[y][x] == OCEAN:
				flowMap[y][x] = END
			elif depthMap[y][x] >= sourceHeight:
					flowMap[y][x] = SOURCE
					flowWeightMap[y][x] = 1
					sources.append({'y':y, 'x':x, 'weight':1})
	print(str(len(sources)) + " sources")
	# flow
	while len(sources) > 0:
		endedFlows = []
		for source in sources:
			print(source)
			flow(source, flowMap, flowWeightMap, depthMap)
			endedFlows.append(source)
		for ended in endedFlows:
			sources.remove(ended)
	# update flowmap
	for y in range(1, height-1): # borders are END by not genuine ones
		for x in range(1, width-1):
			if flowMap[y][x] == END and biomeMap[y][x] == OCEAN:
				Y, X = y, x
				while flowMap[Y][X] != SOURCE:
					biomeMap[Y][X] = RIVER
					if flowMap[Y][X] <= 3:
						flowDir = FLOWDIRECTIONS[flowMap[Y][X]]
						Y, X = Y + flowDir[0], X + flowDir[1]
					else:
						print("error, river goes back to "+str(flowMap[Y][X]))
						break
