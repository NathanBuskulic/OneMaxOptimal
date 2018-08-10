#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 11:36:57 2018

@author: Nathan Buskulic
"""

import numpy as np
import math
import sys

PATH_TO_TABLE = sys.argv[1]  # The size of the OneMax Problem
PATH_TO_WRITE = sys.argv[2]        # The path were we'll write the .npy file


# Optimal parameters for OneMax


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


def optimalOneMax(n,table):
    ''' Return the optimal number of bits to flip at each level (number of ones)
        n : The length of the problem
    '''
    
    bestSoFar = {n:(0,0),n-1:(n,1),0:(1,n)}  #dict who tells us for each level : (The expected time to the solution, The optimal number of bits to flip)
    
    
    for i in range(n-2,0,-1):   #for each level
        
        
        # We get the k we'll use
        k = int(table[i][1])
                    
        mySum = 0
        pTot = 0  #The sum of all probabilities already computed
        
        for j in range(1,min(k,n-i)+1):   #for each amelioration we can hope
            
            p = probabilityGoodFlipLog10(n,k,j,i)
            mySum += p * bestSoFar[i+j][0]
            pTot += p
        
        mySum += 1  # We add the iteration
        
        mySum = mySum * (1/pTot) # We solve the equation
    
        bestSoFar[i] = (mySum,k)
        
    # Compute the global estimated time
    mySum = 0
    for i in range(0,n+1):
        mySum += 10**(log10BinomCoef(n,i) - n * np.log10(2)) * bestSoFar[i][0]
    bestSoFar['Expected Time General'] = (mySum,'All')
    
    return bestSoFar



table = np.load(PATH_TO_TABLE).item()
SIZE = len(table) - 1


# We compute the list we are going to use for the probability
tabLog = np.cumsum(np.log10(np.arange(1,SIZE+1)))

# We compute the optimal solution
opti = optimalOneMax(SIZE,table)

#We save the result:
np.save(PATH_TO_WRITE,opti)
