#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:09:31 2018

@author: Nathan
"""

import numpy as np
import math
from multiprocessing import Pool
#from threading import Thread
#import scipy._lib.messagestream
import scipy.optimize as opti
#import sys




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

#def allAmeliorationProba(n):
#    ''' Return all the Pr[f(y) = f(x) + j] for each i,k and j possible
#        Warning : Long to compute and heavy impact on memory but can save a lot of time
#        n : The size of the problem
#    '''
#    result = {}
#    for i in range(1,n+1):
#        result[i] = {}
#        for k in range(1,n+1):
#            result[i][k] = {}
#            for j in range(1,min(k,n-i)+1):
#                result[i][k][j] = probabilityGoodFlipLog10(n,k,j,i)
#                
#    return result

def optimalOneMax(n):
    ''' Return the optimal number of bits to flip at each level (number of ones)
        n : The length of the problem
    '''
    
    bestSoFar = {n:(0,0),n-1:(n,1)}  #dict who tells us for each level : (The expected time to the solution, The optimal number of bits to flip)
    
    
    for i in range(n-2,0,-1):   #for each level
        
        minTmp = -1 # The best estimated time we've found until now
        index = -1  # The k that gave us minTmp
        
        for k in range(1,n+1):     #for each possible number of flip
            
            mySum = 0
            pTot = 0  #The sum of all probabilities already computed
            
            for j in range(1,min(k,n-i)+1):   #for each amelioration we can hope
                
                p = probabilityGoodFlipLog10(n,k,j,i)
                mySum += p * bestSoFar[i+j][0]
                pTot += p
            
            mySum += 1  # We add the iteration
            
            if pTot != 0:
                mySum = mySum * (1/pTot) # We solve the equation
                
                if mySum < minTmp or minTmp == -1:  #If it's the best solution yet
                    minTmp = mySum
                    index = k
        
        bestSoFar[i] = (minTmp,index)
        
    # We compute the expected time in general
    mySum = 0
    for i in range(1,n+1):
        mySum += 10**(log10BinomCoef(n,i) - n * np.log10(2)) * bestSoFar[i][0]
    bestSoFar['Expected Time General'] = (mySum,'All')
    return bestSoFar
    
    #return bestSoFar
    
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
    
    num = 0
    den = 0
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
        #print(approxP,table[i],i)
        if approxP == 1:
            bestSoFar[i] = (1 + bestSoFar[n-i][0],1)
        else:
            trueP = opti.newton(derivFunction,approxP,args=(n,i,bestSoFar))
            bestSoFar[i] = (basicFunction(n,trueP,i,bestSoFar),trueP)
      
    # We compute the expected time in general
    mySum = 0
    for i in range(1,n+1):
        mySum += 10**(log10BinomCoef(n,i) - n * np.log10(2)) * bestSoFar[i][0]
    bestSoFar['Expected Time General'] = (mySum,'All')
    return bestSoFar

def computeBothTables(n):
    ''' The function that will be threaded to compute everything way faster'''
    print("j'ai démarré avec "+str(n))
    optiOneMax = optimalOneMax(n)
    print("Finished for RLS with n = "+str(n))
    optiEA = optimalEA(optiOneMax,n)
    print("Finished for EA with n = "+str(n))
    np.save("optimalRLS-"+str(n),optiOneMax)
    #print("done with the"+str(n)+"problem !")
    np.save("optimalEA-"+str(n),optiEA)
    print("done with the"+str(n)+"problem !")
    return n
    

tabLog = np.cumsum(np.log10(np.arange(1,20000+1)))
print("done computing the tablog")
pool = Pool(8)
results = pool.map(computeBothTables,list(range(2000,10000,500)))
print(results)
#PATH_TO_WRITE = ""
#for i in range(100,150,10):
#    re
    
#SIZE = int(sys.argv[1])  # The size of the OneMax Problem
        # The path were we'll write the .npy file



#allAmelioration = allAmeliorationProba(SIZE)



