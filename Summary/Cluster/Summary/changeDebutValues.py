#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 10:35:08 2018

@author: Nathan
"""

import numpy as np
import sys

PATH_TO_RLS = sys.argv[1]
PATH_TO_EA = sys.argv[2]

tableRLS = np.load(PATH_TO_RLS).item()
tableEA = np.load(PATH_TO_EA).item()

SIZE = len(tableRLS) - 1
i = SIZE - 1

while tableRLS[i][1] == 1:
    tableEA[i] = (10789,1/(SIZE**2))
    print(i,tableRLS[i])
    i-=1
    
np.save(PATH_TO_EA,tableEA)
