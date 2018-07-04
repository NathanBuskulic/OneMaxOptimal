#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 11:20:16 2018

@author: Nathan
"""

import pandas as pd
import numpy as np
import sys

directory = sys.argv[1]
PATH_TO_WRITE = sys.argv[2]

RLSopt = np.load(directory + 'RLS-opt.npy').item()
EAopt = np.load(directory + 'EA-opt.npy').item()
fulldrift = np.load(directory + 'full-drift.npy').item()
pdrift = np.load(directory + 'p-drift-2.npy').item()
pSup0Drift = np.load(directory + 'p-Sup0-drift-2.npy').item()
pSup0Opt = np.load(directory + 'p-Sup0-opt.npy').item()

monDict = {}
for i in range(500,0,-1):
    monDict[i] = [RLSopt[i][1], RLSopt[i][0], 
                  EAopt[i][1], EAopt[i][0], 
                  fulldrift[i][1], fulldrift[i][0], 
                  pdrift[i][1], pdrift[i][0],
                  pSup0Opt[i][1], pSup0Opt[i][0],
                  pSup0Drift[i][1], pSup0Drift[i][0]]
    
columns = ['RLS-opt','T[RLS-opt]',
           'p-opt','T[p-opt]',
           'RLS-drift','t[RLS-drift]',
           'p-drift','T[p-drift]',
           'p-opt{>0}','T[p-opt{>0}]',
           'p-drift{>0}','T[p-drift{>0}]']

dt = pd.DataFrame.from_dict(monDict,orient='index')
dt.index = list(np.arange(1,501)[::-1])
dt.columns = columns
dt.to_csv(PATH_TO_WRITE,sep=',')

