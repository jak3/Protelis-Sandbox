# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 11:37:52 2016

@author: matte
"""

import numpy as np
import matplotlib.pyplot as plt
import os.path

def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)

def getHeatmap(data, indexes, resolution, startx, starty, endx, endy):
    res = np.zeros(((endx - startx) / resolution, (endy - starty) / resolution))
    i, j = -1, -1
    for x in np.linspace(startx, endx, (endx - startx) / resolution):
        i += 1
        j = -1
        for y in np.linspace(starty, endy, (endy - starty) / resolution):
            j += 1
            res[i][j] = data[int(indexes[i][j])][2]
            if (res[i][j] > 0): 
                res[i][j] = 2000
            if (res[i][j] == -1):
                res[i][j] = 1000
            if (res[i][j] == 0):
                res[i][j] = 0
    return res

def getIndexes(coords, resolution, startx, starty, endx, endy):
    if (False & os.path.exists("data/resourceAllocation_heatmap_raw/indexes.txt")):
        return np.genfromtxt("data/resourceAllocation_heatmap_raw/indexes.txt", dtype=int, delimiter=' ')
    else:
        res = np.zeros(((endx - startx) / resolution, (endy - starty) / resolution))
        i, j = -1, -1
        for x in np.linspace(startx, endx, (endx - startx) / resolution):
            i += 1
            j = -1
            for y in np.linspace(starty, endy, (endy - starty) / resolution):
                j += 1
                res[i][j] = closest_node([y, x], coords)
        np.savetxt('data/resourceAllocation_heatmap_raw/indexes.txt', res, delimiter=' ')
        return res

data = np.genfromtxt("data/resourceAllocation_heatmap_raw/resourceAllocation2.txt", dtype=float, delimiter=' ')
startx, starty, endx, endy = 0, 0, 5, 7
print(endx)
resolution = 0.4
'''
csv format
time steps deviceNum [posX poy]^deviceNum program1^deviceNum program2^deviceNum
'''
offset = 3 #skyp time steps deviceNum
lastRow = data[-1,offset:]
deviceNum = int(data[-1, 2])
x, y = np.array(lastRow[0:deviceNum*2:2]), np.array(lastRow[1:deviceNum*2:2])
offset = deviceNum*2
heatmap1 = np.array(list(zip(x, y, lastRow[offset:offset+deviceNum])))
offset += deviceNum
heatmap2 = list(zip(x, y, lastRow[offset:]))
indexes = getIndexes(list(zip(x, y)), resolution, startx, starty, endx, endy)
figure_size=(10, 10)
plt.figure(figsize=figure_size)

ax0 = plt.subplot(211)
d = getHeatmap(heatmap1, indexes, resolution, startx, starty, endx, endy)
from scipy import ndimage
#ndimage.gaussian_filter1d(d, 10, 1)
ax0.imshow(ndimage.uniform_filter1d(d, 2, 0), cmap='viridis', interpolation='gaussian')
ax0.set_title('Resource allocation map')
#ax1.tick_params(axis='both', which='major', labelsize=int(axissize*0.8))
ax0.grid(b = True, which = 'both')
ax0.set_ylabel("x")
ax0.set_xlabel("y")

ax1 = plt.subplot(212)
ax1.imshow(getHeatmap(heatmap2, indexes, resolution, startx, starty, endx, endy), cmap='viridis', interpolation='gaussian')
ax1.set_title('Resource allocation map')
#ax1.tick_params(axis='both', which='major', labelsize=int(axissize*0.8))
ax1.grid(b = True, which = 'both')
ax1.set_ylabel("x")
ax1.set_xlabel("y")
plt.show()