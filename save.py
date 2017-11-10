import png
import numpy as np
from PIL import Image

def saveMap(m, filename, divratio=1):
	height, width = len(m), len(m[0])
	image = Image.new("P", (height,width))
	y = np.asarray(m)#[m[y][x] for y,x in np.ndindex((height,width))])
	# Convert y to 16 bit unsigned integers.
	z = (65535*((y - y.min())/y.ptp())).astype(np.uint16)
	print(type(z))
	print(z.shape)
	#image.putdata(sequence)
	#image.save(filename)
	# Here's a grayscale example.
	zgray = z#[:, :, 0]

	# Use pypng to write zgray as a grayscale PNG.
	with open(filename, 'wb') as f:
	    writer = png.Writer(width=z.shape[1], height=z.shape[0], bitdepth=16, greyscale=True)
	    zgray2list = zgray.tolist()
	    writer.write(f, zgray2list)