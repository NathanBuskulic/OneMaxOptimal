#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 11:26:39 2018

@author: Nathan
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

# We get the tables
TABK = np.load(sys.argv[1]).item() #np.load("../Summary/1000/RLS-opt.npy").item()
TABP = np.load(sys.argv[2]).item() #np.load("../Summary/1000/p-Sup0-opt-2.npy").item()
PATHTOWRITE = sys.argv[3]

# We get the gap from the middle if needed and deduce the boundary of our datas
if len(sys.argv) >= 5:
    ecartFromMiddle = int(sys.argv[4])
    print(ecartFromMiddle)
    borneInf = int((len(TABK)-1)/2 - ecartFromMiddle)
    print(borneInf)
    borneSup = int((len(TABK)-1)/2 + ecartFromMiddle)
else:
    borneInf = 0
    borneSup = len(TABK) - 1

# We get the datas
dataK = list(TABK.values())[borneInf:borneSup]
dataK = [x[1]/(len(TABK)-1) for x in dataK]

dataP = list(TABP.values())[borneInf:borneSup]
dataP = [x[1] for x in dataP]

xPoints = list(range(borneInf,borneSup))

# We plot everything and save the figure
plt.step(xPoints,dataK,label="k*")
plt.plot(xPoints,dataP,label="p*-Sup0")
plt.legend()
plt.savefig(PATHTOWRITE)
