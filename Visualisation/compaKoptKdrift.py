#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 12:05:49 2018

@author: Nathan
"""

import numpy as np
import matplotlib.pyplot as plt

kopt = np.load('../Summary/2000/RLS-opt.npy').item()
kdrift = np.load('../Summary/2000/full-drift.npy').item()


x = list(range(975,1100))
optValues = [kopt[i][1] for i in x]
driftValues = [kdrift[i][1] for i in x]

plt.step(x,optValues,label='dynamic RLS-opt')
plt.step(x,driftValues,label='dynamic RLS-drift')
plt.legend()
plt.plot()