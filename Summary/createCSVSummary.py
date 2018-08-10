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
baeck = np.load(directory + 'baeck.npy').item()
oldRLS = np.load(directory + 'oldRLS.npy').item()
oldEA = np.load(directory + 'old1+1EA.npy').item()
oldEASup0 = np.load(directory + 'old1+1Sup0.npy').item()
# New Ones
staticP = np.load(directory + 'staticP-final.npy').item()
pSup0driftMedBound = np.load(directory + 'p-Sup0-drift-medBound-2.npy').item()
pSup0driftHighBound = np.load(directory + 'p-Sup0-drift-highBound-2.npy').item()
pSup0optMedBound = np.load(directory + 'p-Sup0-opt-medBound.npy').item()
pSup0optHighBound = np.load(directory + 'p-Sup0-opt-highBound.npy').item()
oldEALowerBound = np.load(directory + 'old1+1Sup0-lowerBound.npy').item()



monDict = {}
for i in range(len(RLSopt)-2,0,-1):
    monDict[i] = [RLSopt[i][1], RLSopt[i][0], 
                  fulldrift[i][1], fulldrift[i][0],
                  pSup0Opt[i][1], pSup0Opt[i][0],
                  pSup0Drift[i][1], pSup0Drift[i][0],
                  EAopt[i][1], EAopt[i][0],  
                  pdrift[i][1], pdrift[i][0],
                  baeck[i][1], baeck[i][0],
                  oldRLS[i][1], oldRLS[i][0],
                  oldEA[i][1], oldEA[i][0],
                  oldEASup0[i][1], oldEASup0[i][0],
                  
                  staticP[i][1], staticP[i][0],
                  pSup0driftMedBound[i][1], pSup0driftMedBound[i][0],
                  pSup0driftHighBound[i][1], pSup0driftHighBound[i][0],
                  pSup0optMedBound[i][1], pSup0optMedBound[i][0],
                  pSup0optHighBound[i][1], pSup0optHighBound[i][0],
                  oldEALowerBound[i][1], oldEALowerBound[i][0]]
                  
    
columns = ['dynamic-RLS-opt','T[dynamic-RLS-opt]',
           'dynamic-RLS-drift','T[dynamic-RLS-drift]',
           'dynamic-(1+1){>0}-p-opt','T[dynamic-(1+1){>0}-p-opt]',
           'dynamic-(1+1){>0}-p-drift','T[dynamic-(1+1){>0}-p-drift]',
           'dynamic-(1+1)-p-opt','T[dynamic-(1+1)-p-opt]',
           'dynamic-(1+1)-p-drift','T[dynamic-(1+1)-p-drift]',
           'dynamic-(1+1)-Baeck','T[dynamic-(1+1)-Baeck]',
           'static-RLS-1','T[static-RLS-1]',
           'static-(1+1)-1/n','T[static-(1+1)-1/n]',
           'old-1+1{>0}','T[old-1+1{>0}]',
           
           'static-(1+1)-opt','T[static-(1+1)-opt]',
           'dynamic-(1+1){>0}-p-drift-1/2n','T[dynamic-(1+1){>0}-p-drift-1/2n]',
           'dynamic-(1+1){>0}-p-drift-1/n','T[dynamic-(1+1){>0}-p-drift-1/n]',
           'dynamic-(1+1){>0}-p-opt-1/2n','T[dynamic-(1+1){>0}-p-opt-1/2n]',
           'dynamic-(1+1){>0}-p-opt-1/n','T[dynamic-(1+1){>0}-p-opt-1/n]',
           'old-1+1{>0}-1/2n','T[old-1+1{>0}-1/2n]']

dt = pd.DataFrame.from_dict(monDict,orient='index')
dt.index = list(np.arange(1,len(RLSopt)-1)[::-1])
dt.columns = columns
dt.to_csv(PATH_TO_WRITE,sep=',')

