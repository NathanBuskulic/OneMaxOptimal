#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 14:51:34 2018

@author: Nathan
"""

import numpy as np
import math
import sys

#PATH_TO_NON_OPTIMAL = sys.argv[1]  # The table of "optimal" results
SIZE = int(sys.argv[1])
PATH_TO_WRITE = sys.argv[2]        # The path were we'll write the .npy file


def log10BinomCoef(n,k):
    ''' Return the Log10 binomial coefficient of n and k
    '''
    
    global tabLog
    
    if k == 0 or k == n:
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
    
    
    combinationZeroes = log10BinomCoef(n-i,nbZeroesToFlip)
    combinationOnes =  log10BinomCoef(i,nbOnesToFlip)
    totalComb =  log10BinomCoef(n,k)
    
    result = combinationZeroes + combinationOnes - totalComb 
    return 10**result


def optimalOneMax(n):
    ''' Return the optimal number of bits to flip at each level (number of ones)
        n : The length of the problem
    '''
    
    bestSoFar = {n:(0,0), n-1:(n,1)}  #dict who tells us for each level : (The expected time to the solution, The optimal number of bits to flip)
    progress = {}
    
    for i in range(n-2,0,-1):   #for each level
        
        minTmp = -1
        index = -1
        progressList = []
        
        for k in range(1,n+1):     #for each possible number of flip
            
            mySum = 0
            pTot = 0
            for j in range(1,min(k,n-i)+1):   #for each amelioration we can hope
                p = probabilityGoodFlipLog10(n,k,j,i)
                mySum += p * bestSoFar[i+j][0]
                pTot += p
            
            mySum += 1  # We add the iteration
            if pTot != 0:
                mySum = mySum * (1/pTot) # We solve the equation
                
                progressList.append(mySum)
                if mySum < minTmp or minTmp == -1:
                    minTmp = mySum
                    index = k
        
        bestSoFar[i] = (minTmp,index)
        progress[i] = progressList
    
    return (bestSoFar,progress)







# We compute the list we are going to use for the probability
tabLog = np.cumsum(np.log10(np.arange(1,SIZE+1)))

# We compute the optimal solution
opti,progressOpti = optimalOneMax(SIZE)

#We save the result:
np.save(PATH_TO_WRITE,progressOpti)

    