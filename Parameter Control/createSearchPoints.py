#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 10:50:12 2018

@author: Nathan
"""

import numpy as np
import sys

SIZE = int(sys.argv[1])
NBRUN = int(sys.argv[2])
PATH_TO_WRITE = sys.argv[3]

result = []
for i in range(NBRUN):
    result.append(np.random.randint(2,size=SIZE))
    
np.save(PATH_TO_WRITE,result)