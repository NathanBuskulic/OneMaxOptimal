#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 10:19:22 2018

@author: Nathan
"""

import numpy as np
import pandas as pd
import sys

PATH_TABLE = sys.argv[1]
PATH_TO_WRITE = sys.argv[2]

table = np.load(PATH_TABLE)
#print(len(table[:,1]))
result = pd.DataFrame({'optimal':table[:,0],'\"optimal\"':table[:,1]})
#result.columns = ['Expected time','k^*']

ind = np.arange(len(table),len(table)*2)
result.index = ind

#print(result)
result.to_csv(PATH_TO_WRITE)