#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 12:14:02 2018

@author: Nathan Buskulic
"""


import numpy as np
import math
import scipy.optimize as opti
import sys

PATH_TO_TABLE = sys.argv[1]

table = np.load(PATH_TO_TABLE).item()
print('WOUHOU----------------------------------------------------------------')
print(table)
SIZE = len(table)-2

PATH_TO_WRITE = sys.argv[2]

if len(sys.argv) >= 4:
    lowerBound = float(sys.argv[3])
else:
    lowerBound = 1/(SIZE**2)


tabLog = np.cumsum(np.log10(np.arange(1,SIZE+1)))



def log10BinomCoef(n,k):
    ''' Return the Log10 binomial coefficient of n and k
    '''
    
    global tabLog
    
    if k <= 0 or k >= n:
        return 0
    
    else:
        return tabLog[n-1] - tabLog[k-1] - tabLog[n-k-1]
    
    

def probabilityGoodFlipLog10(n,k,j,i):
    ''' Return the probability that for a OneMax problem we pass from i ones to i + j ones with k flips using a log10 Binomial coefficient
        n : The length of our OneMax problem
        k : The number of flips
        j : The amount of progress we wish to see
        i : The actual number of ones that we have found
    '''
    
    # if it's impossible
    if (k-j) % 2 == 1:
        return 0.0
    
    
    nbOnesToFlip =  math.ceil( (k - j) / 2 )    # The number of ones to flip to have the result
    nbZeroesToFlip = j + nbOnesToFlip           # The number of zeroes to flip
    
    if nbZeroesToFlip > n-i or nbOnesToFlip > i: # If it's makes no sense
        return 0
    
    
    combinationZeroes = log10BinomCoef(n-i,nbZeroesToFlip)
    combinationOnes =  log10BinomCoef(i,nbOnesToFlip)
    totalComb =  log10BinomCoef(n,k)
    
    result = combinationZeroes + combinationOnes - totalComb 
    return 10**result

   
def binomialLawSup0(n,p,k):
    ''' Return P(X = k) if P follow a bin law such as Bin(n,p) and that 0 can't be taken '''
    if p == 0 or p == 1 or k==0:
        return 0
    else:
        result = log10BinomCoef(n,k) + k * np.log10(p) + (n-k) * np.log10(1-p) - np.log10(1 - ((1-p)**n))
        return 10**result
        
    

def basicFunction(p,n,i):
    ''' Compute the expected time to reach the optimum in a oneMax problem 
    of size n with a 1+1EA using p at the iteration i '''
    
    num = 0
    for k in range(1,n+1):
        tmpN = 0
        for j in range(1,min(k,n-i)+1):
            probaGood = probabilityGoodFlipLog10(n,k,j,i)
            
            tmpN += probaGood * j
        
        binL = binomialLawSup0(n,p,k)
        
        num += binL * tmpN
        
    return  -1 * num




def optimalEA(table,n):
    ''' Return a dict with the optimal parameters to use (1+1)EA
        table : an already optimal table for RLS
        n : the size of the problem
    '''
    bestSoFar = {n:(0,0)}
    
    for i in range(n-1,0,-1):
        if table[i][1] == n:
            bestSoFar[i] = (1 + bestSoFar[n-i][0],1)
        elif table[i][1] == 1:
            trueP = lowerBound
            bestSoFar[i] = (basicFunction(trueP,n,i),trueP)
        else:
            trueP = opti.minimize_scalar(basicFunction,args=tuple([n,i]),bounds=[0,1],method='bounded')
            bestSoFar[i] = (10789,max(trueP.x,lowerBound))
      
    return bestSoFar

# Compute and save the data
np.save(PATH_TO_WRITE,optimalEA(table,SIZE))
