#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 09:37:36 2018

@author: Nathan
"""

import numpy as np
import pandas as pd
import sys

PATH_TABLE = sys.argv[1]
PATH_TO_WRITE = sys.argv[2]

table = np.load(PATH_TABLE)
#print(table)
result = pd.DataFrame.from_dict(table.item(),orient='index')
result.columns = ['Expected time','k^*']

#ind = np.arange(1,len(table.item()) + 1)[::-1]
ind = list(table.item().keys())
result.index = ind
ind = ['Expected Time General'] + ind[:-1]
result = result.reindex(ind)
result.to_csv(PATH_TO_WRITE,sep="\t")