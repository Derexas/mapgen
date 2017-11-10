from opensimplex import OpenSimplex as simplexnoise
import numpy as np

def noise(gen, nx, ny):
	# Rescale from -1.0:+1.0 to 0.0:1.0
	return gen.noise2d(nx, ny) / 2.0 + 0.5


def add_noise(gen, array, octave, weight=1, decaly=0, decalx=0):
	height, width = len(array), len(array[0])
	for y in range(height):
		for x in range(width):
			nx = octave*(x/width - 0.5 + decalx)
			ny = octave*(y/height - 0.5 + decaly)
			array[y][x] += weight*noise(gen, 8*nx, 8*ny)


def gaussian_kernel(height, width, sigma=32):
	sigma = sigma * (height/128)
	x0, y0 = height/2, width/2,
	x, y = np.arange(width), np.arange(height)

	gx = np.exp(-(x-x0)**2/(2*sigma**2))
	gy = np.exp(-(y-y0)**2/(2*sigma**2))
	g = np.outer(gx, gy)
	#g /= np.sum(g)	# normalize, if you want that # no thx
	g *= 1.4
	return g