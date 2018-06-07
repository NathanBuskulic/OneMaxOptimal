#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 10:52:14 2018

@author: Nathan
"""

import numpy as np
import sys

PATH_TABLE = sys.argv[1]
PATH_TO_WRITE = sys.argv[2]


def log10BinomCoef(n,k):
    ''' Return the Log10 binomial coefficient of n and k
    '''
    
    global tabLog
    
    if k == 0 or k == n:
        return 0
    else:
        return tabLog[n-1] - tabLog[k-1] - tabLog[n-k-1]
    
    
def theoreticalResults(table):
    ''' Return the theoretical results of the given table
    '''
    SIZE = len(table)
    result = {}
    names = ['statique','\"optimal\"','optimal']
    for name in range(len(names)):
        mySum = 0
        for i in range(1,SIZE+1):
            #print(i,name,table[])
            mySum += 10**(log10BinomCoef(SIZE,i) - SIZE * np.log10(2)) * table[i][name][0]
        result[names[name]] = mySum
    return result
        
        
# load tables
tables = np.load(PATH_TABLE).item()
#print(tables)     
        
n = len(tables)
tabLog = np.cumsum(np.log10(np.arange(1,n+1)))
res = theoreticalResults(tables)
np.save(PATH_TO_WRITE,res)
