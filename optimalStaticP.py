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
#import matplotlib.pyplot as plt

SIZE = int(sys.argv[1])
PATH_TO_WRITE = sys.argv[2]
#SIZE = 500
#table = np.load(PATH_TO_TABLE).item()
#SIZE = len(table)
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
    
    
def basicFunction(n,p,i,bestSoFar,binTable):
    
    global allAmelioration
    
    num = 0
    den = 0
    for k in range(1,n+1):
        tmpN = 0
        tmpD = 0
        for j in range(1,min(k,n-i)+1):
            probaGood = allAmelioration[i][k][j] #probabilityGoodFlipLog10(n,k,j,i)
            
            tmpN += probaGood * bestSoFar[i+j][0]
            tmpD += probaGood
            #print("boucle j :",probaGood,tmpN,tmpD)
        binL = binTable[k]#binomialLaw(n,p,k)
        #binL = binomialLaw(n,p,k)
        num += binL * tmpN
        den += binL * tmpD
       # print("boucle k :",binL,tmpN,tmpD)
    num += 1
    #print(num,den,binL)        
    return num/den


def derivFunction(p,n,i,bestSoFar,binTableDeriv,binTable):
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
          
        binL = binTable[k]
        binLDeriv = binTableDeriv[k]
        
        u += binL * tmpU
        uPrime += binLDeriv * tmpU
        v += binL * tmpV
        vPrime += binLDeriv * tmpV
        
    u += 1
    return ((uPrime * v) - (u * vPrime)) / (v**2)

def allSolutionsProba(n):
    ''' return all the probability to start with that solution
        n : the size of the problem
    '''
    
    result = {}
    for i in range(1,n+1):
        result[i] = 10**(log10BinomCoef(n,i) - n * np.log10(2))
    
    return result

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


def allBinomial(n,p):
    ''' Return all the derivative of Bin(n,p) = k results (for each k of course)
        n : the size of the problem
        p : the probability to have a good flip
    '''
    
    result = {}
    for k in range(1,n+1):
        result[k] = binomialLaw(n,p,k)
    return result


def allBinomialDeriv(n,p):
    ''' Return all the derivative of Bin(n,p) = k results (for each k of course)
        n : the size of the problem
        p : the probability to have a good flip
    '''
    
    result = {}
    for k in range(1,n+1):
        result[k] = binomialLawDeriv(n,p,k)
    return result


def basicOptimalP(p,n):
    
    binTable = allBinomial(n,p)
    bestSoFar = {n:(0,0)}
    for i in range(n-1,0,-1):
        bestSoFar[i] = (basicFunction(n,p,i,bestSoFar,binTable),p)
    mySum = 0
    for i in range(1,SIZE+1):
        mySum += allSolutionsProb[i] * bestSoFar[i][0]
    return mySum

#def derivOptimalP(p,n):
#    ''' Return the derivative of the function that gives the optimal p (we want to find the root)
#        p : the probability of flipping a bit
#        n : the size of the problem
#    '''
##    #global allSolutionsProb
##    
##    # We compute the binomial law tab
##    binTableDeriv = allBinomialDeriv(n,p)
##    binTable = allBinomial(n,p)
##    #print(allSolutionsProb)
##    
##    
##    # our expected time with that p
##    bestSoFar = {n:(0,0)}
##    deriv = {n:derivFunction(p,n,n,bestSoFar,binTableDeriv,binTable)}
##    result = 0
##    for i in range(n-1,0,-1):
##        bestSoFar[i] = (basicFunction(n,p,i,bestSoFar,binTable),p)
##        deriv[i] = derivFunction(p,n,i,bestSoFar,binTableDeriv,binTable)
##        #derivFunction()
##    #print(bestSoFar)
##    for i in range(1,n):
##        #deriv = derivFunction(p,n,i,bestSoFar,binTableDeriv,binTable)
##        #print("allSoluceProbas :",allSolutionsProb[i])
##        #print("deriv :",deriv)
##        result += (allSolutionsProb[i] * deriv[i])
##        print(allSolutionsProb[i],deriv[i])
##    print("result :",result)   
##    return result
#    
#    binTable = allBinomial(n,p)
#    binDeriv = allBinomialDeriv(n,p)
#    
#    fullResultTable = {n:(0,0)}
#    # On remplit la table
#    for i in range(n-1,0,-1):
#        fullResultTable[i] = (basicFunction(n,p,i,fullResultTable,binTable),p)
#    
#    mySum = 0
#    for i in range(1,n):
#        mySum += (10**(log10BinomCoef(n,i) - n * np.log10(2))) * derivFunction(p,n,i,fullResultTable,binDeriv,binTable)
#    
#    return mySum
#    #return basicOptimalP(p,n) - basicOptimalP(p+0.000001,n)
    
    
def optimalP(n):
    ''' Return a dict with the optimal parameters to use (1+1)EA with a static p
        n : the size of the problem
    '''
    global allSolutionsProb
    
    #approxP = 1/n
    #trueP = opti.newton(derivOptimalP,approxP,args=(tuple([n])))
    trueP = opti.minimize_scalar(basicOptimalP,bracket=(1/(2*n),1/n,1/(0.5*n)),args=(tuple([n])))
    #print(trueP)
    #bestSoFar = basicOptimalP(n,trueP)
    
    # We compute the expected time in general
    #mySum = 0
    #for i in range(1,SIZE+1):
    #    mySum += allSolutionsProb[i] * bestSoFar[i][0]
    #bestSoFar['Expected Time General'] = (mySum,'All')
    #return bestSoFar
    return (trueP.x,trueP.fun)

allSolutionsProb = allSolutionsProba(SIZE)
allAmelioration = allAmeliorationProba(SIZE)



best = optimalP(SIZE)
np.save(PATH_TO_WRITE,best)

