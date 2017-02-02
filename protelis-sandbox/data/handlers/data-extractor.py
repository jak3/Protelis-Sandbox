# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 16:37:01 2016

@author: wabo
"""

inputDirectory = "data/vip_raw/"
outputDirectory = "data/vip/"
inputName = "vip"
outputName = inputName

'''
inputDirectory = "data/resourceAllocation_raw/"
outputDirectory = "data/resourceAllocation/"
inputName = "resourceAllocation"
outputName = inputName
'''

'''
inputDirectory = "data/resourceAllocationNaive_raw/"
outputDirectory = "data/resourceAllocation/"
inputName = "resourceAllocation"
outputName = "resourceAllocationNaive"
'''

import numpy as np
import os  # need os for working with files
# This module provides support for Unix shell-style wildcards, which are not the same as regular expressions 
# (which are documented in the re module). The special characters used in shell-style wildcards are:
# *     matches everything
# ?     matches any single character
# [seq]     matches any character in seq
# [!seq]     matches any character not in seq
import fnmatch
import re
import csv
f = open(outputDirectory + outputName + '-dump.csv', 'w')
writer = csv.writer(f, delimiter=' ', lineterminator='\n')
seedVar = "random"

def convFloat(x, limit='inf'):
    try:
        result = float(x)
        if result == float('inf') or result == float('-inf') or result > limit:
            return float('NaN')
        return result
    except ValueError:
        return float('NaN')

def lineToArray(line):
    return [convFloat(x, limit = 10e6) for x in line.split()]

def openCsv(path):
    with open(path, 'r') as file:
        lines = filter(lambda x: re.compile('\d').match(x[0]), file.readlines())
        return [lineToArray(line) for line in lines]

def getVariableValue(var, file):
    match = re.search('(?<=' + var + '-)\d+(\.\d*)?', file)
    return match.group(0)

def computeData(simulations):
    OFFSET = 3    
    res = []
    for s in simulations:
        simulation = s[1]
        lastRow = simulation[-1]
        earlierMatch = []#lastRow
        for i in range(1, len(simulation) - 1, 1):
            if (np.nan_to_num(lastRow[OFFSET:]) == np.nan_to_num(simulation[-i][OFFSET:])).all():
                earlierMatch = simulation[-i]
            else:
                break
        print([re.split(inputName, s[0])[1], earlierMatch[2], earlierMatch[0]])
        writer.writerow([re.split(inputName, s[0])[1], earlierMatch[2], earlierMatch[0]])
        res.append([earlierMatch[2], earlierMatch[0]])
    return res

allfiles = list(filter(lambda file: fnmatch.fnmatch(file, '*_' + seedVar + '-*.txt'), os.listdir(inputDirectory)))
floatre = '[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
split = list(set(tuple(re.split('_'+ seedVar +'-'+ floatre, x)) for x in allfiles))

mJoin = []
meanJoin = []

for descriptor in split:
    print(descriptor)
    writer.writerow(str(descriptor))
    unixMatch = descriptor[0] + '*' + descriptor[2]
    matchingFiles = filter(lambda f: fnmatch.fnmatch(f, unixMatch), os.listdir(inputDirectory))   
    contents = [[file, openCsv(inputDirectory + '/' + file)] for file in matchingFiles]
    data = computeData(contents)
    print(str(np.nanstd(data, axis=0)))
    mJoin.append(np.append(np.nanmean(data, axis=0), np.nanstd(data, axis=0)[1]))

meanJoin = sorted(mJoin, key=lambda x: x[0])
print("--- final")
print("--- deviceNumber meanTime stdTime")
print(meanJoin)
np.savetxt(outputDirectory + outputName + '-mean-err.txt', meanJoin, delimiter=' ')
f.close()