#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:48:18 2018

@author: Nathan
"""


#import sys
import subprocess as subp


#PATH_TO_NON_OPTIMAL = sys.argv[1]  # The table of "optimal" results
PATH_TO_WRITE = "../"        # The path were we'll write the .npy file

# Add the / at the end of the path if it doesn't exist
#if PATH_TO_NON_OPTIMAL[-1] != '/':
#    PATH_TO_NON_OPTIMAL += '/'
    
#if PATH_TO_WRITE[-1] != '/':
#    PATH_TO_WRITE += '/'
    
for i in range(100,150,40):
    subp.call(['python','../createOptimalTable.py', str(i), PATH_TO_WRITE + 'optimalTableRLS'+str(i)])
    subp.call(['python','../optimal1+1EA.py', PATH_TO_WRITE + 'optimalTableRLS'+str(i)+'.npy', PATH_TO_WRITE + 'optimal1+1EA'+str(i)])
    print("just finished the computation for "+str(i)+" !")