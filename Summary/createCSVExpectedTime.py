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

STOP_POINT = int(sys.argv[1])
PATH_TO_WRITE = sys.argv[2]


result = {}
directory = '100/'
number = 100
while number <= STOP_POINT and os.path.exists(directory):
    tabLog = np.cumsum(np.log10(np.arange(1,number+1)))
    
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
    
    
    
    result[number] = [RLSopt['Expected Time General'][0],
                      fulldrift['Expected Time General'][0],
                      pSup0Opt['Expected Time General'][0],
                      pSup0Drift['Expected Time General'][0],
                      EAopt['Expected Time General'][0],
                      pdrift['Expected Time General'][0],
                      baeck['Expected Time General'][0],
                      oldRLS['Expected Time General'][0],
                      oldEA['Expected Time General'][0],
                      oldEASup0['Expected Time General'][0],
                      
                      staticP[1][1],
                      staticP['Expected Time General'][0],
                      pSup0driftMedBound['Expected Time General'][0],
                      pSup0driftHighBound['Expected Time General'][0],
                      pSup0optMedBound['Expected Time General'][0],
                      pSup0optHighBound['Expected Time General'][0],
                      oldEALowerBound['Expected Time General'][0]]
    
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
           'E[old-1+1{>0}]',
           
           'static-(1+1)-opt',
           'E[static-(1+1)-opt]',
           'E[dynamic-(1+1){>0}-p-drift-1/2n]',
           'E[dynamic-(1+1){>0}-p-drift-1/n]',
           'E[dynamic-(1+1){>0}-p-opt-1/2n]',
           'E[dynamic-(1+1){>0}-p-opt-1/n]',
           'E[old-1+1{>0}-1/2n]']


dt.columns = columns
dt.to_csv(PATH_TO_WRITE,sep=',')