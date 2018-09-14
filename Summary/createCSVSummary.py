#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 11:20:16 2018

@author: Nathan
"""

import pandas as pd
import numpy as np
import sys
import os

directory = sys.argv[1]
PATH_TO_WRITE = sys.argv[2]

#A dict of correspondance between the columns name and the file where we can find the data
correspondence = {'dynamic-RLS-opt' : {'fileName':'RLS-opt.npy'},
                  'dynamic-RLS-drift' : {'fileName':'full-drift.npy'},
                  'dynamic-(1+1){>0}-p-opt' : {'fileName':'p-Sup0-opt.npy'},
                  'dynamic-(1+1){>0}-p-drift' : {'fileName':'p-Sup0-drift-2.npy'},
                  'dynamic-(1+1)-p-opt' : {'fileName':'EA-opt.npy'},
                  'dynamic-(1+1)-p-drift' : {'fileName':'p-drift-2.npy'},
                  'dynamic-(1+1)-Baeck' : {'fileName':'baeck.npy'},
                  'static-RLS-1' : {'fileName':'oldRLS.npy'},
                  'static-(1+1)-1/n' : {'fileName':'old1+1EA.npy'},
                  'old-1+1{>0}' : {'fileName':'old1+1Sup0.npy'},
                  'static-(1+1)-opt' : {'fileName':'staticP-final.npy'},
                  'dynamic-(1+1){>0}-p-drift-1/2n' : {'fileName':'p-Sup0-drift-medBound-2.npy'},
                  'dynamic-(1+1){>0}-p-drift-1/n' : {'fileName':'p-Sup0-drift-highBound-2.npy'},
                  'dynamic-(1+1){>0}-p-opt-1/2n' : {'fileName':'p-Sup0-opt-medBound.npy'},
                  'dynamic-(1+1){>0}-p-opt-1/n' : {'fileName':'p-Sup0-opt-highBound.npy'},
                  'old-1+1{>0}-1/2n' : {'fileName':'old1+1Sup0-lowerBound.npy'}}

# We load the data we have
for column in list(correspondence.keys()):
    if os.path.isfile(directory+correspondence[column]['fileName']):
        # If the file exists we load the data
        correspondence[column]['data'] = np.load(directory + correspondence[column]['fileName']).item()
    else:
        # We delete that column
        del correspondence[column]


# We get the size of the data
size = len(correspondence[list(correspondence.keys())[0]]['data'])-2


monDict = {}
for i in range(size,0,-1):
    
    listTmp = []
    for column in correspondence:
        listTmp.append(correspondence[column]['data'][i][1])
        listTmp.append(correspondence[column]['data'][i][0])
    monDict[i] = listTmp
    
    
# We get the column's name
columns = []
for column in correspondence:
    columns.append(column)
    columns.append('T['+column+']')

dt = pd.DataFrame.from_dict(monDict,orient='index')
dt.index = list(np.arange(1,size+1)[::-1])
dt.columns = columns
dt.to_csv(PATH_TO_WRITE,sep=',')

