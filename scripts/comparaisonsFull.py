#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 11:13:36 2018

@author: Nathan
"""

import numpy as np
import sys

PATH_STATIQUE = sys.argv[1]
PATH_EDUARDO = sys.argv[2]
PATH_OPTIMAL = sys.argv[3]
PATH_TO_WRITE = sys.argv[4]

statique = np.load(PATH_STATIQUE)
statique = statique.item()
eduardo = np.load(PATH_EDUARDO)
eduardo = eduardo.item()
optimal = np.load(PATH_OPTIMAL).item()
#optimal = optimal.item()

result = {}
for key in statique:
    result[key] = [statique[key],eduardo[key],optimal[key]]

np.save(PATH_TO_WRITE,result)
