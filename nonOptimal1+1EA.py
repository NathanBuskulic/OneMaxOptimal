#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 14:15:11 2018

@author: Nathan
"""

import numpy as np
import math
import scipy.optimize as opti
import sys
#import matplotlib.pyplot as plt

#PATH_TO_TABLE = sys.argv[1]
PATH_TO_WRITE = sys.argv[2]

#table = np.load(PATH_TO_TABLE).item()
#SIZE = len(table)
SIZE = int(sys.argv[1])
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
    
    if p <= 0 or p >= 1:
        return 0
    else:
        result = log10BinomCoef(n,k) + k * np.log10(p) + (n-k) * np.log10(1-p)
        return 10**result
    
    
def binomialLawDeriv(n,p,k):
    ''' return the derivative of P(X = k) if P follow a binomial Law such as Bin(n,p)
        n : The number of experiment
        p : probability of success
        k : the number we want to reach
    '''
    
    if p <= 0 or p >= 1:
        return 0
    else:
        result = log10BinomCoef(n,k) + (k-1) * np.log10(p) + (n-k-1) * np.log10(1-p)
        return (10**result) * (k - (p*n))
    
    
def basicFunction(n,p,i):
    
    if p <= 0 or p >= 1:
        print("TU FAIS QUOI ?")
    num = 0
    den = 0
    for k in range(1,n+1):
        tmpN = 0
        tmpD = 0
        for j in range(1,min(k,n-i)+1):
            probaGood = probabilityGoodFlipLog10(n,k,j,i)
            
            tmpN += probaGood * j
            tmpD += probaGood
        
        binL = binomialLaw(n,p,k)
        
        num += binL * tmpN
        den += binL * tmpD
        
    num += 1
    if den == 0:
        print(p,i,tmpN,tmpD,binL)
    return num/den


def derivFunction(p,n,i):
    ''' Return the derivative of the function that find the optimal parameter
        n : the size of the problem
        p : the probability
        i : the number of ones
        bestSoFar : results we already have
    '''
    #if p < 0:
        #return 0
    
    u, uPrime, v, vPrime = 0, 0, 0, 0
    for k in range(1,n+1):
        
        tmpU, tmpV = 0, 0
        for j in range(1,min(k,n-i)+1):
            probaGoodFlip = probabilityGoodFlipLog10(n,k,j,i)
            
            tmpU += probaGoodFlip * j
            tmpV += probaGoodFlip
          
        binL = binomialLaw(n,p,k)
        binLDeriv = binomialLawDeriv(n,p,k)
        
        u += binL * tmpU
        uPrime += binLDeriv * tmpU
        v += binL * tmpV
        vPrime += binLDeriv * tmpV
        
    u += 1
    #print(v,tmpV,p,n,i,(uPrime * v - u * vPrime) / pow(v,2))
    return (uPrime * v - u * vPrime) / pow(v,2)


def nonOptimalEA(n):
    ''' Return a dict with the optimal parameters to use (1+1)EA
        table : an already optimal table for RLS
        n : the size of the problem
    '''
    bestSoFar = {n:(0,0)}
    
    for i in range(n-1,0,-1):
        #approxP = 1 / (2*i + 2 - n )
        approxP = 1 / n
        #print(approxP,i)
        #print(table[i])
        #if table[i][1] == (n-1):
            #print('WOLO')
        #    bestSoFar[i] = (1 + bestSoFar[n-i][0],1)
        #else:
            #a = 0.001
            #a = 1/n
            #print(a)
            #b = 0.55
            #b = (n-200)/n
            #print(a,b)
            #print(b)
        trueP = opti.newton(derivFunction,approxP,args=(n,i))
            #print(trueP)
        bestSoFar[i] = (basicFunction(n,trueP,i) + bestSoFar[i+1][0],trueP)
        print(i,bestSoFar[i])
     
    # We compute the expected time in general
    mySum = 0
    for i in range(1,SIZE+1):
        mySum += 10**(log10BinomCoef(SIZE,i) - SIZE * np.log10(2)) * bestSoFar[i][0]
    bestSoFar['Expected Time General'] = (mySum,'All')
    return bestSoFar


#table = np.load('tables/eduardoFull/eduardoFull500.npy').item()
best = nonOptimalEA(SIZE)
np.save(PATH_TO_WRITE,best)
#listeP = np.linspace(0.003,0.1,100)
#l = []
#for p in listeP:
#    l.append(derivFunction(p,SIZE,270))
    
#    
#plt.plot(listeP,l)
#np.save(PATH_TO_WRITE,nonOptimalEA(table,SIZE))