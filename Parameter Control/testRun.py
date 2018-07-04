#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 11:26:39 2018

@author: Nathan
"""

import numpy as np
from Algos import AdaptativePursuit
from Algos import DynamicUCB
from Algos import MutationChange
from Algos import RLSMutationChange
from Problem import OneMaxProblem

p = OneMaxProblem(5000)
a = AdaptativePursuit(100,0.001,0.8,0.8,p)
d = DynamicUCB(0.08,0.1,p)
c = MutationChange(1.5,0.5,0.1,p)
e = RLSMutationChange(5,0.1,0.0001,p)
c.run()
#print(c.getResults())
print(c.getResults())