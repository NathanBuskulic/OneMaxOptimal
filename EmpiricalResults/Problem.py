#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 15:41:52 2018

@author: Nathan
"""

import numpy as np

class Problem:
    
    def __init__(self,n):
        self.size = n
        
    def step(self,k):
        pass
    
    def isDone(self):
        pass
    
class OneMaxProblem(Problem):
    def __init__(self,n,startPoint = []):
        ''' Initialisation du problème'''
        self.size = n
        if len(startPoint) == 0:
            self.vector = np.random.randint(2,size=self.size)
        else:
            self.vector = startPoint
        
    def step(self,k):
        ''' flip k bits of the problem '''
        #We get the bits we'll flip
        toFlip = np.random.choice(self.size,k,replace=False)
        
        badFlip = sum([self.vector[i] for i in toFlip])
        # If we'll flip more ones into zeroes than the contrary, we return 0
        if badFlip >= k/2:
            return 0
        
        else:
            #We flip the bits
            for i in toFlip:
                self.vector[i] = (self.vector[i] + 1)%2
            return k - badFlip
        
    def isDone(self):
        return sum(self.vector) == self.size
    
    def getState(self):
        return sum(self.vector)