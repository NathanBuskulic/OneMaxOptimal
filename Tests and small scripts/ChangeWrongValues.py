#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 11:13:40 2018

@author: Nathan
"""

import numpy as np

tab = np.load('../Summary/2000/p-Sup0-drift.npy').item()
norm = tab[1918][1]

for i in range(1936,2000):
    tab[i] = (10789,norm)
    
np.save('../Summary/2000/p-Sup0-drift.npy',tab)
