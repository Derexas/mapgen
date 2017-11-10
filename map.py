from matplotlib import pyplot as plt
import random
import time
from save import saveMap
from height import heightMap
from height import addNoise
from biome import moistureMap
from biome import biomeMap
from rivers2 import drainageBasins
from rivers2 import flowMap
from rivers2 import flatMap
from rivers2 import flowHeatMap
from rivers2 import lakesMap

seed1 = 795483475248761111;
seed2 = 982793098977361;

MULT = 1
height, width = 128*MULT+1, 128*MULT+1
t = time.time()
heightmap = heightMap(height, width, seed1)
moisturemap = moistureMap(height, width, seed2)
flowmap = flowMap(heightmap)
basinsmap = flatMap(flowmap)
drainagebasins,drains = drainageBasins(heightmap, flowmap)
flowheatmap = flowHeatMap(flowmap[0])
lakesmap,waterhmap = lakesMap(heightmap, drainagebasins, drains, flowheatmap,flowmap[0])
biomemap = biomeMap(heightmap, moisturemap,lakesmap)

print((time.time()-t)*1000, "ms")

saveMap(heightmap, "heightmap.png")
saveMap(waterhmap, "waterhmap.png")
saveMap(biomemap, "biomemap.png", divratio=14)

fig = plt.figure()
a=fig.add_subplot(1,3,1)
imgplot = plt.imshow(waterhmap)
a.set_title('Flow map')
plt.colorbar(orientation ='horizontal')#ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13], 
a=fig.add_subplot(1,3,2)
imgplot = plt.imshow(biomemap)
a.set_title('Flat')
plt.colorbar(orientation='horizontal')#ticks=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1], 
a=fig.add_subplot(1,3,3)
imgplot = plt.imshow(heightmap)
a.set_title('Drain map')
plt.colorbar(orientation='horizontal')

#plt.gray()
plt.show()