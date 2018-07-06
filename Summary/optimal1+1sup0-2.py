#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 11:12:16 2018

@author: Nathan
"""

import numpy as np
import math
import scipy.optimize as opti
import sys
#import matplotlib.pyplot as plt

PATH_TO_TABLE = sys.argv[1]
PATH_TO_WRITE = sys.argv[2]

table = np.load(PATH_TO_TABLE).item()
#print(table)
SIZE = len(table) - 1
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

def allAmeliorationProba(n):
    ''' Return all the Pr[f(y) = f(x) + j] for each i,k and j possible
        Warning : Long to compute and heavy impact on memory but can save a lot of time
        n : The size of the problem
    '''
    result = {}
    for i in range(1,n+1):
        result[i] = {}
        for k in range(1,n+1):
            result[i][k] = {}
            for j in range(1,min(k,n-i)+1):
                result[i][k][j] = probabilityGoodFlipLog10(n,k,j,i)
                
    return result

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
    
def binomialLawDeriv(n,p,k):
    ''' return the derivative of P(X = k) if P follow a binomial Law such as Bin(n,p)
        n : The number of experiment
        p : probability of success
        k : the number we want to reach
    '''
    
    if p == 0 or p == 1:
        return 0
    else:
        result = log10BinomCoef(n,k) + (k-1) * np.log10(p) + (n-k-1) * np.log10(1-p)
        return (10**result) * (k - (p*n))
  
def binomialLawDerivSup0(n,p,k):
    ''' return the derivative of P(X = k) if P follow a binomial Law such as Bin(n,p) and 0 can't be choose
        n : The number of experiment
        p : probability of success
        k : the number we want to reach
    '''
    
    if p == 0 or p == 1 or k == 0:
        return 0
    else:
        u = binomialLaw(n,p,k)
        uPrime = binomialLawDeriv(n,p,k)
        v = 1 - pow(1-p,n)
        vPrime = n * (1-p)**(n-1)
        result = (uPrime * v - vPrime * u) / pow(v,2)
        return result
    

def basicFunction(p,n,i,bestSoFar):
    
    global allAmelioration
    p = max(p,1/(n**2))
    
    num = 0
    den = 0
    for k in range(1,n+1):
        tmpN = 0
        tmpD = 0
        for j in range(1,min(k,n-i)+1):
            probaGood = allAmelioration[i][k][j]
            
            tmpN += probaGood * bestSoFar[i+j][0]
            tmpD += probaGood
        
        binL = binomialLawSup0(n,p,k)
        
        num += binL * tmpN
        den += binL * tmpD
        
    num += 1        
    return num/den


def derivFunction(p,n,i,bestSoFar):
    ''' Return the derivative of the function that find the optimal parameter
        n : the size of the problem
        p : the probability
        i : the number of ones
        bestSoFar : results we already have
    '''
    global allAmelioration
    
    u, uPrime, v, vPrime = 0, 0, 0, 0
    for k in range(1,n+1):
        
        tmpU, tmpV = 0, 0
        for j in range(1,min(k,n-i)+1):
            probaGoodFlip = allAmelioration[i][k][j]
            
            tmpU += probaGoodFlip * bestSoFar[i+j][0]
            tmpV += probaGoodFlip
          
        binL = binomialLawSup0(n,p,k)
        binLDeriv = binomialLawDerivSup0(n,p,k)
        
        u += binL * tmpU
        uPrime += binLDeriv * tmpU
        v += binL * tmpV
        vPrime += binLDeriv * tmpV
        
    u += 1
    return (uPrime * v - u * vPrime) / pow(v,2)


def optimalEA(table,n):
    ''' Return a dict with the optimal parameters to use (1+1)EA
        table : an already optimal table for RLS
        n : the size of the problem
    '''
    bestSoFar = {n:(0,0)}
    
    for i in range(n-1,0,-1):
        approxP = table[i][1] / n
        print(approxP)
        #print(approxP,table[i],i)
        if approxP == 1:
            bestSoFar[i] = (1 + bestSoFar[n-i][0],1)
        else:
            #print(i)
            trueP = opti.minimize_scalar(basicFunction,args=(n,i,bestSoFar),bounds=[0,1],method='bounded')
            print(i,trueP)
            trueP.x = max(trueP.x,1/(n**2))
            bestSoFar[i] = (basicFunction(trueP.x,n,i,bestSoFar),trueP.x)
      
    # We compute the expected time in general
    mySum = 0
    for i in range(1,SIZE+1):
        mySum += 10**(log10BinomCoef(SIZE,i) - SIZE * np.log10(2)) * bestSoFar[i][0]
    bestSoFar['Expected Time General'] = (mySum,'All')
    return bestSoFar

allAmelioration = allAmeliorationProba(SIZE)
#print("DONE !")
#print(SIZE)
np.save(PATH_TO_WRITE,optimalEA(table,SIZE))