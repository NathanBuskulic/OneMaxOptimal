#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 14:39:29 2018

@author: Nathan
"""

import sys
import subprocess as subp


PATH_TO_NON_OPTIMAL = sys.argv[1]  # The table of "optimal" results
PATH_TO_WRITE = sys.argv[2]        # The path were we'll write the .npy file

# Add the / at the end of the path if it doesn't exist
if PATH_TO_NON_OPTIMAL[-1] != '/':
    PATH_TO_NON_OPTIMAL += '/'
    
if PATH_TO_WRITE[-1] != '/':
    PATH_TO_WRITE += '/'
    
for i in range(3000,4001,500):
    subp.call(['python','../main.py', PATH_TO_NON_OPTIMAL+'r_table_n'+str(i)+'.npy', PATH_TO_WRITE + 'tableScriptComp'+str(i)])
    