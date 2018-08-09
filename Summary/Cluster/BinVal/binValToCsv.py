#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 15:50:15 2018

@author: Nathan
"""

import numpy as np
import sys
import pandas as pd
import math

PATH_TO_TABLE = sys.argv[1]
PATH_TO_WRITE = sys.argv[2]

def binOfInt(n):
    ''' Return the binary representation of the integer n '''
    #print(n)
    monBin = bin(n)[2:]
    result = [0 for i in range(SIZE - len(monBin))]
    for i in monBin:
        result.append(int(i))
    return result


table = np.load(PATH_TO_TABLE).item()
SIZE = math.ceil(np.log2(len(table) - 1))
result = {'Expected Time General':['NaN' for i in range(SIZE)]+[table['Expected Time General'][0],table['Expected Time General'][1]]}
#table = np.load(PATH_TO_TABLE).item()
del table['Expected Time General']

#SIZE = math.ceil(np.log2(max(table.keys(),key=lambda x:int(x))))


columns = ['#bit' + str(SIZE - i) for i in range(SIZE)]+['Expected Time', 'k-opt']
for i in range(2**SIZE-1,-1,-1):
    #binstring = '#'
    #for j in binOfInt(i):
    #    binstring += str(j)
    binrep = binOfInt(i)
    result[i] = binrep + [table[i][0],table[i][1]]
    
dt = pd.DataFrame.from_dict(result,orient='index')
dt.columns = columns
dt.to_csv(PATH_TO_WRITE)
