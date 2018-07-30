#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 13:59:24 2018

@author: Nathan
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opti
import sys


def func(x,a,b):
    #print(x,a,b,c)
    return 1 / (a * x + b)
    #return (a * x + b) / c

# We get the datas
tablePStar = np.load("../Summary/3500/p-Sup0-opt.npy").item()
SIZE = len(tablePStar) - 1

# We arange our datas so that we can use them
x = list(range(SIZE//2,SIZE))
y = list(tablePStar.values())[SIZE//2:-1]
y = [x[1] for x in y]

# We get the curve fit
popt, pcov = opti.curve_fit(func,x,y)

# We plot it alongside the optimal p*-Sup0
plt.plot(x,y)
newLab = [func(x1, *popt) for x1 in x]
plt.plot(x,y,'b-', label="p*-Sup0")
plt.plot(x, newLab, 'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
plt.legend()
plt.savefig("curveFit-3500.png")
 