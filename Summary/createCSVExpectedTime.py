#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 12:15:02 2018

@author: Nathan
"""

import pandas as pd
import os
import numpy as np
import sys

PATH_TO_WRITE = sys.argv[1]



def log10BinomCoef(n,k):
    ''' Return the Log10 binomial coefficient of n and k
    '''
    
    global tabLog
    
    if k <= 0 or k >= n:
        return 0
    
    else:
        return tabLog[n-1] - tabLog[k-1] - tabLog[n-k-1]
    

def computeExpectedTime(table,size):
    mySum = 0
    for i in range(1,size+1):
        mySum += 10**(log10BinomCoef(size,i) - size * np.log10(2)) * table[i][0]
    return mySum

result = {}
directory = '100/'
number = 100
while os.path.exists(directory):
    tabLog = np.cumsum(np.log10(np.arange(1,number+1)))
    
    RLSopt = np.load(directory + 'RLS-opt.npy').item()
    EAopt = np.load(directory + 'EA-opt.npy').item()
    fulldrift = np.load(directory + 'full-drift.npy').item()
    fulldrift['Expected Time General'] = (computeExpectedTime(fulldrift,len(fulldrift)),'all')
    pdrift = np.load(directory + 'p-drift-2.npy').item()
    pSup0Drift = np.load(directory + 'p-Sup0-drift-2.npy').item()
    pSup0Opt = np.load(directory + 'p-Sup0-opt.npy').item()
    baeck = np.load(directory + 'baeck.npy').item()
    oldRLS = np.load(directory + 'oldRLS.npy').item()
    oldEA = np.load(directory + 'old1+1EA.npy').item()
    oldEASup0 = np.load(directory + 'old1+1Sup0.npy').item()
    staticpOpt = np.load(directory + 'static-p.npy')
    
    result[number] = [RLSopt['Expected Time General'][0],
                      fulldrift['Expected Time General'][0],
                      pSup0Opt['Expected Time General'][0],
                      pSup0Drift['Expected Time General'][0],
                      EAopt['Expected Time General'][0],
                      pdrift['Expected Time General'][0],
                      baeck['Expected Time General'][0],
                      oldRLS['Expected Time General'][0],
                      oldEA['Expected Time General'][0],
                      staticpOpt[1],
                      staticpOpt[0],
                      oldEASup0['Expected Time General'][0]]
    
    if number != 100:
        number += 500
    else:
        number = 500
    directory = str(number) + '/'
    
dt = pd.DataFrame.from_dict(result,orient='index')
columns = ['E[dynamic-RLS-opt]',
           'E[dynamic-RLS-drift]',
           'E[dynamic-(1+1){>0}-p-opt]',
           'E[dynamic-(1+1){>0}-p-drift]',
           'E[dynamic-(1+1)-p-opt]',
           'E[dynamic-(1+1)-p-drift]',
           'E[dynamic-(1+1)-Baeck]',
           'E[static-RLS-1]',
           'E[static-(1+1)-1/n]',
           'E[static-(1+1)-p*]',
           '(1+1)-p*',
           'E[old-1+1{>0}]']
dt.columns = columns
dt.to_csv(PATH_TO_WRITE,sep=',')