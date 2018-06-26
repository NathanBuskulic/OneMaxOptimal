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
from Problem import OneMaxProblem

p = OneMaxProblem(100)
a = AdaptativePursuit(100,0.001,0.8,0.8,p)
d = DynamicUCB(0.08,0.1,p)
c = MutationChange(1.5,0.5,0.1,p)
c.run()
print(c.results)
print(len(c.results))