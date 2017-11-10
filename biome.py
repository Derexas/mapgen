from noise import *

def moistureMap(height, width, seed):
	moisturemap = []
	gen = simplexnoise(seed);
	for i in range(height):
		moisturemap.append([0 for x in range(width)])
	add_noise(gen, moisturemap, 2, 1, decaly=100, decalx=100)
	return moisturemap

OCEAN = 0; OCEAN = 0; RIVER = 1; BEACH = 2; SCORCHED = 3; BARE = 4; TUNDRA = 5; SNOW = 6
TEMPERATE_DESERT = 7; SHRUBLAND = 8; GRASSLAND = 7; TEMPERATE_DECIDUOUS_FOREST = 8
TEMPERATE_RAIN_FOREST = 9; SUBTROPICAL_DESERT = 10; TROPICAL_SEASONAL_FOREST = 11;
TAIGA = 12; TROPICAL_RAIN_FOREST = 13

def biome(e, m):
	if (e < 0.2):
		return OCEAN
	if (e < 0.22):
		return BEACH
	
	if e > 0.8:
		if (m < 0.1):
			return SCORCHED
		if (m < 0.2):
			return BARE
		if (m < 0.5):
			return TUNDRA
		return SNOW

	if (e > 0.6):
		if (m < 0.33):
			return TEMPERATE_DESERT
		if (m < 0.66):
			return SHRUBLAND
		return TAIGA

	if (e > 0.3):
		if (m < 0.16):
			return TEMPERATE_DESERT
		if (m < 0.50):
			return GRASSLAND
		if (m < 0.83):
			return TEMPERATE_DECIDUOUS_FOREST
		return TEMPERATE_RAIN_FOREST

	if m < 0.16:
		return SUBTROPICAL_DESERT
	if m < 0.33:
		return GRASSLAND
	if m < 0.66:
		return TROPICAL_SEASONAL_FOREST
	return TROPICAL_RAIN_FOREST

def biomeMap(heightmap, moisturemap,lakesmap):
	height, width = len(heightmap), len(heightmap[0])
	riverid = len(lakesmap)-1
	biomemap = []
	for y in range(height):
		bml = []
		for x in range(width):
			if lakesmap[y][x] > 0:
				bml.append(RIVER)
			else:
				bml.append(biome(heightmap[y][x], moisturemap[y][x]))
		biomemap.append(bml)
	return biomemap