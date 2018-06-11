#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:57:53 2018

@author: Nathan
"""

import numpy as np
import math
import scipy as sp
import matplotlib.pyplot as plt

table = np.load('tables/optimal/100.npy').item()
SIZE = len(table)
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
    
    if nbZeroesToFlip > n-i or nbOnesToFlip > i:
        return 0
    
    
    combinationZeroes = log10BinomCoef(n-i,nbZeroesToFlip)
    combinationOnes =  log10BinomCoef(i,nbOnesToFlip)
    totalComb =  log10BinomCoef(n,k)
    
    result = combinationZeroes + combinationOnes - totalComb 
    return 10**result


#def sommeProba(n,p,j,i):
#    
#    for k in range(1,n+1):
#        mySum = 0
#        if k >= j and (k-j)%2 == 0:
#            
#            nbOnesToFlip =  math.ceil( (k - j) / 2 )    # The number of ones to flip to have the result
#            nbZeroesToFlip = j + nbOnesToFlip           # The number of zeroes to flip
#                
#            mySum += pow(p,k) * pow(1-p,n-k) * (10**(log10BinomCoef(n-i,nbZeroesToFlip) + log10BinomCoef(i,nbOnesToFlip)))
#    
#    return mySum

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
    
def basicFunction(n,p,i,bestSoFar):
    
    numerator = 0
    tmp = 0
    for k in range(1,n+1):
        tmp = 0
        for j in range(1,min(k,n-i)+1):
            tmp += probabilityGoodFlipLog10(n,k,j,i) * bestSoFar[i+j][0]
        
        numerator += binomialLaw(n,p,k) * (tmp) 
        
    numerator += 1
    denom = 0
    tmp = 0
    for k in range(1,n+1):
        tmp = 0
        for j in range(1,min(k,n-i)+1):
            #print('proba :',probabilityGoodFlipLog10(n,k,j,i),n,k,j,i)
            #print('tmp avant :',tmp)
            tmp += probabilityGoodFlipLog10(n,k,j,i)
        
        #print('tmp',tmp,n,k,j,i,p)
        denom += binomialLaw(n,p,k) * tmp 
        
    #print('final:',denom)
    return numerator/denom


def derivFunction(p,n,i,bestSoFar):
    ''' Return the derivative of the function that find the optimal parameter
        n : the size of the problem
        p : the probability
        i : the number of ones
        bestSoFar : results we already have
    '''
    
    u, uPrime, v, vPrime = 0, 0, 0, 0
    for k in range(1,n+1):
        
        tmpU, tmpV = 0, 0
        for j in range(1,min(k,n-i)+1):
            probaGoodFlip = probabilityGoodFlipLog10(n,k,j,i)
            
            tmpU += probaGoodFlip * bestSoFar[i+j][0]
            tmpV += probaGoodFlip
          
        binL = binomialLaw(n,p,k)
        binLDeriv = binomialLawDeriv(n,p,k)
        
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
        if approxP == 1:
            bestSoFar[i] = (1 + bestSoFar[n-i][0],1)
        else:
            #print(i,table[i])
            trueP = sp.optimize.newton(derivFunction,approxP,args=(n,i,bestSoFar))
            bestSoFar[i] = (basicFunction(n,trueP,i,bestSoFar),trueP)
            #print(bestSoFar[i])
        
    return bestSoFar

print(optimalEA(table,SIZE))
    

#def sommeProbaDeriv(n,p,j,i):
#    for k in range(1,n+1):
#        mySum = 0
#        if k >= j and (k-j)%2 == 0:
#            nbOnesToFlip =  math.ceil( (k - j) / 2 )    # The number of ones to flip to have the result
#            nbZeroesToFlip = j + nbOnesToFlip           # The number of zeroes to flip
#            
#            mySum += pow(p,k-1) * pow(1-p,n-k-1) * (1 - p*(n-k-1)) * (10**(log10BinomCoef(n-i,nbZeroesToFlip) + log10BinomCoef(i,nbOnesToFlip)))
#    
#    return mySum



#def derivFunction(p,n,i,bestSoFar):
#    ''' Return the derivative of the function we want to minimize
#        p : the probability to use in the binomial law
#        n : the size of the problem
#        i : the number of one
#    '''
#    
#    result = 0
#    num = 0
#    denom = 0
#    
#    for j in range(1,n+1-i):
#        num += sommeProbaDeriv(n,p,j,i)
#        denom += sommeProba(n,p,j,i)
#        print(denom)
#    
#    result = -1 * (num / pow(denom,2))
#    
#    
#    tmp = 0
#    for j in range(1,n+1-i):
#        tmp += sommeProba(n,p,j,i) * bestSoFar[i+j][0]
#    tmp += 1
#    
#    result = result * tmp
#    
#    tmp = 0
#    for j in range(1,n+1-i):
#        tmp += sommeProba(n,p,j,i)
#    
#    resultTmp = 1/tmp
#    
#    tmp = 0
#    for j in range(1,n+1-i):
#        tmp += sommeProbaDeriv(n,p,j,i) * bestSoFar[i+j][0]
#    resultTmp = resultTmp * tmp
#    
#    result += resultTmp
#    
#    return result
#
#def functionBasique(n,p,i,bestSoFar):
#    result = 0
#    tmp = 0
#    for j in range(1,n-i+1):
#        tmp += sommeProba(n,p,j,i)
#    
#    result = 1/tmp
#    tmp = 0
#    
#    for j in range(1,n-i+1):
#        tmp += sommeProba(n,p,j,i) * bestSoFar[i+j][0]
#    tmp += 1
#    result = result * tmp
#    
#    return result
#p
    
#listeRes = []
#bestSoFar = {100:(0,0),99:(100,0)}
#sep = np.linspace(0.001,0.150,500)
#for p in sep:
#    #print(p) 
#    listeRes.append(derivFunction(SIZE,p,98,bestSoFar))
#
#listeRes = [abs(i) for i in listeRes]
#print(listeRes)
#print(listeRes.index(min(listeRes)), sep[listeRes.index(min(listeRes))])
##print(listeRes[30],listeRes[58:65])
#plt.plot(sep,listeRes)
    
#print(binomialLawDeriv(10,0.5,5))
    
#print(BinomialLawDeriv(10,0.1,1))
