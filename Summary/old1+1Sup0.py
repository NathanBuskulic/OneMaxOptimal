#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:06:33 2018

@author: Nathan Buskulic
"""


import numpy as np
import math
import sys

SIZE = int(sys.argv[1])
PATH_TO_WRITE = sys.argv[2]

# We get the static p we want to use in our algorithm, if nothing provided, take 1/n
if len(sys.argv) >= 4:
    staticP = float(sys.argv[3])
else:
    staticP = 1/SIZE

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


def binomialLaw(n,p,k):
    ''' return P(X = k) if P follow a binomial Law such as Bin(n,p)
        n : The number of experiment
        p : probability of success
        k : the number we want to reach
    '''
    
    if p == 0 or p == 1:
        return 0
    else:
        result = log10BinomCoef(n,k) + k * np.log10(p) + (n-k) * np.log10(1-p)
        return 10**result
    
    
    
    
def binomialLawSup0(n,p,k):
    ''' Return P(X = k) if P follow a bin law such as Bin(n,p) and that 0 can't be taken '''
    if p <= 0 or p >= 1 or k==0:
        return 0
    else:
        #print(p,k,1 - pow((1-p),n),pow((1-p),n))
        result = log10BinomCoef(n,k) + k * np.log10(p) + (n-k) * np.log10(1-p) - np.log10(1 - pow((1-p),n))
        return 10**result
    
    
def basicFunction(n,p,i,bestSoFar):
    ''' Compute the expected time to reach the optimum in a oneMax problem 
    of size n with a 1+1EA using p at the iteration i '''
    num = 0
    den = 0
    for k in range(1,n+1):
        tmpN = 0
        tmpD = 0
        for j in range(1,min(k,n-i)+1):
            probaGood = probabilityGoodFlipLog10(n,k,j,i)
            
            tmpN += probaGood * bestSoFar[i+j][0]
            tmpD += probaGood
        
        binL = binomialLawSup0(n,p,k)
        
        num += binL * tmpN
        den += binL * tmpD
        
    num += 1        
    return num/den




def optimalEA(n):
    ''' Return a dict with the optimal parameters to use (1+1)EA
        table : an already optimal table for RLS
        n : the size of the problem
    '''
    bestSoFar = {n:(0,0)}
    #p = 1/n
    
    for i in range(n-1,0,-1):
        
        bestSoFar[i] = (basicFunction(n,staticP,i,bestSoFar),staticP)
      
    # We compute the expected time in general
    mySum = 0
    for i in range(1,SIZE+1):
        mySum += 10**(log10BinomCoef(SIZE,i) - SIZE * np.log10(2)) * bestSoFar[i][0]
    bestSoFar['Expected Time General'] = (mySum,'All')
    return bestSoFar

# We compute and save the data
np.save(PATH_TO_WRITE,optimalEA(SIZE))