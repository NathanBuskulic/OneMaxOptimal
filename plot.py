#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 14:44:32 2018

@author: Nathan
"""

import numpy as np
import matplotlib.pyplot as plt


PATH_TO_TABLE = "table1000.npy"
table = np.load(PATH_TO_TABLE)
diff = [abs(table[i][0] - table[i][1]) for i in range(len(table))]
axis = list(range(501,1001))
#plt.plot(axis,table[:,0])
#plt.plot(axis,table[:,1])
plt.plot(axis,diff)
