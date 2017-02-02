# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 16:37:01 2016
@author: wabo
"""

outputDirectory = "charts/"
plots = [   
   {"outName": "resourceAllocation", "title": "\"Resource allocation\"", "name": ["resourceAllocation", "resourceAllocationNaive"], "inputDir":"data/resourceAllocation/"},   
   {"outName": "vip","title": "\"Meet the celebrity\"", "name": ["vip"], "inputDir":"data/vip/"}
]
titlesize = 14
axissize = 12
figure_size = (7, 5)

import numpy as np
import matplotlib.pyplot as plt
import os  # need os for working with files
# This module provides support for Unix shell-style wildcards, which are not the same as regular expressions 
# (which are documented in the re module). The special characters used in shell-style wildcards are:
# *     matches everything
# ?     matches any single character
# [seq]     matches any character in seq
# [!seq]     matches any character not in seq
import fnmatch
import re
from scipy.optimize import curve_fit

#cmap = plt.cm.get_cmap('inferno')
colors = ['red', 'blue', 'orange', 'green']

for p in plots:
    #start = 0.1
    start = 0
    #step = 0.5
    step = 1
    chartName = p['title']
    inputDirectory = p['inputDir']
    fig_aggr_ctrl = plt.figure(figsize=figure_size)    
    ax1 = plt.subplot(111)
    for name in p['name']:
        #get data from each file
        join = np.genfromtxt(inputDirectory + name + "-mean-err.txt", dtype=float, delimiter=' ') 
        #print(join)
        X   = np.array([x[0] for x in join])
        Y   = np.array([x[1] for x in join])
        err = np.array([x[2] for x in join])
        # interpolate data
        def f(x, a, b):
            return a * np.sqrt(b * x)
        popt, pcov = curve_fit(f, X, Y)
        #print(popt)
        np.savetxt(inputDirectory + name + '-popt.txt', popt, delimiter=' ')
        Y_fit = f(X, popt[0], popt[1])
        #print(X) print(Y) print(Y_fit)
        #ax1.plot(X, Y_fit, c=cmap(start), label=name + " Fitting curve")
        ax1.plot(X, Y_fit, linestyle='--', color=colors[start], label=name + " fitting curve")
        if (len(p['name']) == 1):
            start = start + step
        #ax1.errorbar(X, Y, err, c=cmap(start), fmt='-o', label=name + " Mean time")
        ax1.errorbar(X, Y, err, color=colors[start], fmt='-o', label=name + " mean time")
        start = start + step
    ax1.set_title(chartName + ' stabilization chart', fontsize=titlesize)
    #ax1.tick_params(axis='both', which='major', labelsize=int(axissize*0.8))
    ax1.grid(b = True, which = 'both')
    ax1.set_ylabel("Simulation time (s)", fontsize=axissize)
    ax1.set_xlabel("Number of devices", fontsize=axissize)
    ax1.set_ylim(ymin=0)
    ax1.set_xlim(xmin=0)
    ax1.legend(loc=4)    
    plt.tight_layout()
    plt.savefig(outputDirectory + p['outName'] + '.pdf')
    plt.show()    