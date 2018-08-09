#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 09:57:32 2018

@author: Nathan
"""

import subprocess as sp
from multiprocessing import Process
import sys
start = int(sys.argv[1])
end = int(sys.argv[2])
PATH_TO_WRITE = sys.argv[3]

python = "python"

def binVal(taille):
    sp.call([python,"optimalbinVal.py",str(taille),PATH_TO_WRITE + "binVal"+str(taille)])
    sp.call([python,"binValToCsv.py",PATH_TO_WRITE + "binVal"+str(taille)+".npy",PATH_TO_WRITE + "binVal"+str(taille)+".csv"])

tabProc = []
for i in range(end - start):
    tabProc.append(Process(target=binVal,args=(start + i,)))
    tabProc[i].start()

for i in range(end - start):    
    tabProc[i].join()
    