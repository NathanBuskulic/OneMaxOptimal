#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 15:51:44 2018

@author: Nathan
"""

from Problem import OneMaxProblem
import numpy as np
import sys

PATH_TO_TABLE = sys.argv[1] # Path to the table with the k to use
SIZE = int(sys.argv[2])
NBRUN = int(sys.argv[3])
NAME = sys.argv[4] # Name to give to the files
PATH_TO_WRITE = sys.argv[5] # The directory where to put everything

if len(sys.argv) >= 7:
    BIN = sys.argv[6] == 'True' # Tell if you're using deterministic values or binomial distribution values
else:
    BIN = False
    
if len(sys.argv) >= 8:
    TABLE_START_POINTS = np.load(sys.argv[7]) # the tables where all the starting points are
else:
    TABLE_START_POINTS = []

table = np.load(PATH_TO_TABLE).item()

# Opening the files
fileData = open(PATH_TO_WRITE+"data_f1/"+NAME+".tdat",'w')
fileInfo = open(PATH_TO_WRITE+NAME+".info",'w')

# First line of fileinfo
myLine = "suite = 'PBO', funcId = 1, DIM = "+str(SIZE)+", algId = '"+NAME+"', IOHProfiler_version = ''\n%\n"
myLine += "data_f1/"+NAME+".dat"
fileInfo.write(myLine)

for i in range(NBRUN):
    # opening the run
    fileData.write('"function evaluation" "original f(x)" "best original f(x)" "transformed f(x) " "best transformed f(x)" "mutation strength"\n')

    # Initializing the one max problem
    if len(TABLE_START_POINTS) == 0:
        oneMax = OneMaxProblem(SIZE)
    else:
        oneMax = OneMaxProblem(SIZE,TABLE_START_POINTS[i])
    iteration = 1
    k = table[oneMax.getState()][1]
    
    #write the first line
    myLine = str(iteration)
    state = oneMax.getState()
    for i in range(4):
        myLine += " " + str(state)
    myLine += " 0"
    fileData.write(myLine+"\n")
    
    while not oneMax.isDone():
        # We do the step
        if not BIN:
            k = table[oneMax.getState()][1]
        else:
            k = np.random.binomial(SIZE,table[oneMax.getState()][1])
        oneMax.step(k)
        iteration += 1
        
        #We write the next line
        myLine = str(iteration)
        state = oneMax.getState()
        for i in range(4):
            myLine += " " + str(state)
        myLine += " " + str(table[oneMax.getState()][1])
        fileData.write(myLine+"\n")

    # When the run is done, writing in the info file
    myLine = ", 1:"+str(iteration)+"|1.00000e+02"
    fileInfo.write(myLine)

#closing the file        
fileData.close()
fileInfo.close()
