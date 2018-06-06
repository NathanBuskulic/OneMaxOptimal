#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 09:14:20 2018

@author: Nathan
"""

import sys
import subprocess as subp


#PATH_TO_NON_OPTIMAL = sys.argv[1]  # The table of "optimal" results
PATH_TO_WRITE = sys.argv[1]        # The path were we'll write the .npy file

# Add the / at the end of the path if it doesn't exist
#if PATH_TO_NON_OPTIMAL[-1] != '/':
#    PATH_TO_NON_OPTIMAL += '/'
    
if PATH_TO_WRITE[-1] != '/':
    PATH_TO_WRITE += '/'
    
for i in range(1500,4001,500):
    subp.call(['python','../createOptimalTable.py', str(i), PATH_TO_WRITE + 'optimalTable'+str(i)])
    