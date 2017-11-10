from noise import *

def heightMap(height, width, seed):
	heightmap = []
	gen = simplexnoise(seed);
	for i in range(height):
		heightmap.append([0 for x in range(width)])

	add_noise(gen, heightmap, 1, 1)
	add_noise(gen, heightmap, 2, 0.5)
	add_noise(gen, heightmap, 3, 0.4)
	#add_noise(gen, heightmap, 4, .2)
	#add_noise(gen, heightmap, 6, .1)
	#add_noise(gen, heightmap, 10, 0.03)
	#add_noise(gen, heightmap, 100, 0.1)

	g_k = gaussian_kernel(height, width) #make the map an island

	height, width = len(heightmap), len(heightmap[0])
	for y in range(height):
		for x in range(width):
			heightmap[y][x] *= g_k[y][x] / (3.23)
	return heightmap

def addNoise(heightmap, seed, freq, intensity):
	gen = simplexnoise(seed);
	add_noise(gen, heightmap, freq, intensity)