#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 11:09:52 2018

@author: Nathan
"""


import numpy as np
import math
import scipy.optimize as opti
import sys

SIZE = int(sys.argv[1])
PATH_TO_WRITE = sys.argv[2]
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
    
    
def basicFunction(n,p,i,bestSoFar,binTable):
    ''' Compute the expected time to reach the optimum in a oneMax problem 
    of size n with a 1+1EA using p at the iteration i '''
    
    num = 0 #numerator
    den = 0 #denominator
    
    for k in range(1,n+1):
        tmpN = 0
        tmpD = 0
        for j in range(1,min(k,n-i)+1):
            probaGood = probabilityGoodFlipLog10(n,k,j,i) 
            
            tmpN += probaGood * bestSoFar[i+j][0]
            tmpD += probaGood

        binL = binomialLaw(n,p,k)
        num += binL * tmpN
        den += binL * tmpD
    num += 1
    return num/den


def allBinomial(n,p):
    ''' Return all the derivative of Bin(n,p) = k results (for each k of course)
        n : the size of the problem
        p : the probability to have a good flip
    '''
    
    result = {}
    for k in range(1,n+1):
        result[k] = binomialLaw(n,p,k)
    return result



def basicOptimalP(p,n):
    ''' Return the global expected time for a n-sized problem with a static 1+1EA using p
        n : size of the problem
        p : value to use with a 1+1EA
    '''
    global bestResult
    
    #Init
    binTable = allBinomial(n,p)
    bestSoFar = {n:(0,0)}
    
    # Computing every values...
    for i in range(n-1,0,-1):
        bestSoFar[i] = (basicFunction(n,p,i,bestSoFar,binTable),p)
        bestResult[i] = bestSoFar[i]
    
    #Compute the global expected time
    mySum = 0
    for i in range(1,SIZE+1):
        mySum += 10**(log10BinomCoef(n,i) - n * np.log10(2)) * bestSoFar[i][0]
    return mySum

    
    
def optimalP(n):
    ''' Return a dict with the optimal parameters to use (1+1)EA with a static p
        n : the size of the problem
    '''
    global bestResult
    
    trueP = opti.minimize_scalar(basicOptimalP,bracket=(1/(2*n),1/n,1/(0.5*n)),args=(tuple([n])))

    bestResult['Expected Time General'] = (trueP.fun,'All')
    return bestResult

# Initialize the global variable that will hold the result
bestResult = {}

# Get the best static p
best = optimalP(SIZE)

#We save the result
np.save(PATH_TO_WRITE,best)

