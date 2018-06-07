#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:11:12 2018

@author: Nathan
"""

import numpy as np
import sys

TABLE = sys.argv[1]
PATH_TO_WRITE = sys.argv[2]

table = np.load(TABLE)
#print(table)
newTable = []
n = len(table)*2

for i in range(0,len(table)):
    v = n//2 - i
    print(v, n//2 + v//2)
    newTable.append(n - table[v-1])
   
#print(table)
result = np.concatenate((newTable,table), axis=0)
#print(result)

print(result)  
#We save the result
np.save(PATH_TO_WRITE,result)