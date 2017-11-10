from noise import *

def moistureMap(height, width):
	biomemap = []
	for i in range(height):
		moisturemap.append([0 for x in range(width)])

	add_noise(gen2, moisturemap, 2, 1, decaly=100, decalx=100)
