#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 11:44:45 2018

@author: Nathan
"""

import numpy as np
import sys


SIZE = int(sys.argv[1])
PATH_TO_WRITE = sys.argv[2]

def valueBinVal(vec):
    ''' Return the integer value of the binary representation vec '''
    return sum([((2**(len(vec) - i - 1)) * vec[i]) for i in range(len(vec))])

def binOfInt(n):
    ''' Return the binomial representation of the integer n '''
    #print(n)
    monBin = bin(n)[2:]
    result = [0 for i in range(SIZE - len(monBin))]
    for i in monBin:
        result.append(int(i))
    return result

def differencesInBin(vec1,vec2):
    ''' Return the number of zeroes and ones to flip to get from vec1 to vec2 '''
   # print(vec1,vec2)
    nbZeroes = 0
    nbOnes = 0
    for i in range(len(vec2)):
        if vec1[i] != vec2[i]:
            if vec1[i] == 0:
                nbZeroes += 1
            else:
                nbOnes += 1
    return (nbZeroes,nbOnes)


def log10BinomCoef(n,k):
    ''' Return the Log10 binomial coefficient of n and k
    '''
    global tabLog
    
    if k == 0 or k == n:
        return 0
    
    else:
        return tabLog[n-1] - tabLog[k-1] - tabLog[n-k-1]

def probaAmelioration(actualState,j,k):
    ''' Return the probability that by flipping k bits we go from actualState to actualState + j '''
    actualStateBin = binOfInt(actualState)
    nbZeroesToFlip, nbOnesToFlip = differencesInBin(actualStateBin,binOfInt((valueBinVal(actualStateBin) + j)))
    #print('proba :', actualState, j, k, nbZeroesToFlip, nbOnesToFlip)
    
    if k != (nbZeroesToFlip + nbOnesToFlip):
        return 0
    
    else:
        #nbOnes = sum(actualStateBin)
        length = len(actualStateBin)
        #nbZeroes = length - nbOnes
        #combZeroes = log10BinomCoef(nbZeroes,nbZeroesToFlip)
        #combOnes = log10BinomCoef(nbOnes,nbOnesToFlip)
        combTot = log10BinomCoef(length,k)
        
        return 1/10**(combTot)
    
def optimalBinVal(n):
    ''' return the optimal number of bits to flip in a binVal problem of size n'''
    
    bestSoFar = {2**n - 1 : (0,0)}
    for i in range(2**n - 2,0,-1):
        minK = -1 #store the minimum k
        valueK = -1 #Store the minimum value associated
        
        for k in range(1,n+1):
            mySum = 0
            pTot = 0
            for j in range(1,2**n-i):
                #print('BWAH :',i,j,k)
                proba = probaAmelioration(i,j,k)
                #print(proba)
                mySum += proba * bestSoFar[i+j][0]
                pTot += proba
                
            mySum += 1
            #print(i,k,mySum,pTot)
            if pTot != 0:
                mySum = mySum / pTot
                
                if mySum < valueK or valueK == -1 :
                    valueK = mySum
                    minK = k
                
        bestSoFar[i] = (valueK,minK)
        
    mySum = 0
    for i in range(1,2**n - 1):
        #print(i,(2**(n)))
        mySum += bestSoFar[i][0]
    bestSoFar['Expected Time General'] = (mySum/len(bestSoFar),'All')
    return bestSoFar
     
tabLog = np.cumsum(np.log10(np.arange(1,2**(SIZE+1))))


best = optimalBinVal(SIZE)
np.save(PATH_TO_WRITE,best)
