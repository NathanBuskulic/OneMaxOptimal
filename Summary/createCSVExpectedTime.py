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
    nameList = ['RLS-opt', 'EA-opt', 'full-drift', 'p-drift-2', 
                'p-Sup0-drift-2', 'p-Sup0-opt', 'baeck', 'oldRLS', 
                'old1+1EA', 'old1+1Sup0', 'staticP-final', 'p-Sup0-drift-medBound-2',
                'p-Sup0-drift-highBound-2', 'p-Sup0-opt-medBound', 'p-Sup0-opt-highBound', 'old1+1Sup0-lowerBound']
    
    data = {}  #The dict that will contains all the data we have for that number
    for name in nameList:
        if os.path.isfile(directory+name+'.npy'):
             #We get the data
             data[name] = np.load(directory + name + '.npy').item()
        else:
            # We create data that will show us that we don't have anything
            if name != 'staticP-final':
                data[name] = {'Expected Time General':[None,]}
            else:
                data[name] = {'Expected Time General':[None,],1:[None,None]}
     
    
    result[number] = [data['RLS-opt']['Expected Time General'][0],
                      data['full-drift']['Expected Time General'][0],
                      data['p-Sup0-opt']['Expected Time General'][0],
                      data['p-Sup0-drift-2']['Expected Time General'][0],
                      data['EA-opt']['Expected Time General'][0],
                      data['p-drift-2']['Expected Time General'][0],
                      data['baeck']['Expected Time General'][0],
                      data['oldRLS']['Expected Time General'][0],
                      data['old1+1EA']['Expected Time General'][0],
                      data['old1+1Sup0']['Expected Time General'][0],
                      
                      data['staticP-final'][1][1],
                      data['staticP-final']['Expected Time General'][0],
                      data['p-Sup0-drift-medBound-2']['Expected Time General'][0],
                      data['p-Sup0-drift-highBound-2']['Expected Time General'][0],
                      data['p-Sup0-opt-medBound']['Expected Time General'][0],
                      data['p-Sup0-opt-highBound']['Expected Time General'][0],
                      data['old1+1Sup0-lowerBound']['Expected Time General'][0]]
    
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