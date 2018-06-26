#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 15:31:31 2018

@author: Nathan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 13:30:10 2018

@author: Nathan
"""

import scipy.special as special
import scipy.optimize as opti
import numpy as np
import math
import sys
import sympy
import copy
import matplotlib.pyplot as plt



#
## Optimal code for OneMax
#
#def probabilityGoodFlip(n,k,j,i):
#    ''' Return the probability that for a OneMax problem we pass from i ones to i + j ones with k flips
#        n : The length of our OneMax problem
#        k : The number of flips
#        j : The amount of progress we wish to see
#        i : The actual number of ones that we have found
#    '''
#    
#    # if it's impossible
#    if (k-j) % 2 == 1:
#        return 0.0
#    
#    
#    nbOnesToFlip =  math.ceil( (k - j) / 2 )    # The number of ones to flip to have the result
#    nbZeroesToFlip = j + nbOnesToFlip           # The number of zeroes to flip
#    
#    combinationZeroes = special.binom((n-i), nbZeroesToFlip)
#    combinationOnes = special.binom( i ,nbOnesToFlip)
#    totalComb = special.binom(n,k)
#    
#    
#    return combinationZeroes / totalComb * combinationOnes
#
#
#
##def probabilityGoodFlipLog10(n,k,j,i):
##    ''' Return the probability that for a OneMax problem we pass from i ones to i + j ones with k flips
##        n : The length of our OneMax problem
##        k : The number of flips
##        j : The amount of progress we wish to see
##        i : The actual number of ones that we have found
##    '''
##    global tabLog
##    
##    # if it's impossible
##    if (k-j) % 2 == 1:
##        return 0.0
##    
##    
##    nbOnesToFlip =  math.ceil( (k - j) / 2 )    # The number of ones to flip to have the result
##    nbZeroesToFlip = j + nbOnesToFlip           # The number of zeroes to flip
##    
##    #tabLog = np.log10(np.arange(1,n))
##    #print(tabLog)
##    combinationZeroes = sum(tabLog[:n-i]) - sum(tabLog[:nbZeroesToFlip]) - sum(tabLog[:n-i-nbZeroesToFlip])
##    combinationOnes =  sum(tabLog[:i]) - sum(tabLog[:nbOnesToFlip]) - sum(tabLog[:i-nbOnesToFlip])
##    totalComb =  sum(tabLog[:n]) - sum(tabLog[:k]) - sum(tabLog[:n-k])
##    
##    result = combinationZeroes + combinationOnes - totalComb 
##    #print("result",10**combinationZeroes)
##    return 10**result
#    
def log10BinomCoef(n,k):
    ''' Return the Log10 binomial coefficient of n and k
    '''
    
    global tabLog
    
    if k == 0 or k == n:
        return 0
    else:
        return tabLog[n-1] - tabLog[k-1] - tabLog[n-k-1]
    
    

def probabilityGoodFlipLog10(n,k,j,i):
    ''' Return the probability that for a OneMax problem we pass from i ones to i + j ones with k flips
        n : The length of our OneMax problem
        k : The number of flips
        j : The amount of progress we wish to see
        i : The actual number of ones that we have found
    '''
    #global tabLog
    
    # if it's impossible
    if (k-j) % 2 == 1:
        return 0.0
    
    
    nbOnesToFlip =  math.ceil( (k - j) / 2 )    # The number of ones to flip to have the result
    nbZeroesToFlip = j + nbOnesToFlip           # The number of zeroes to flip
    
    #tabLog = np.log10(np.arange(1,n))
    #print(tabLog)
    combinationZeroes = log10BinomCoef(n-i,nbZeroesToFlip)
    combinationOnes =  log10BinomCoef(i,nbOnesToFlip)
    totalComb =  log10BinomCoef(n,k)
    
    result = combinationZeroes + combinationOnes - totalComb 
    #print("result",10**combinationZeroes)
    return 10**result
#
#
#
#def optimalOneMax(n):
#    ''' Return the optimal number of bits to flip at each level (number of ones)
#        n : The length of the problem
#    '''
#    
#    bestSoFar = {n:(0,0), n-1:(n,1)}  #dict who tells us for each level : (The expected time to the solution, The optimal number of bits to flip)
#    
#    
#    for i in range(n-2,1,-1):   #for each level
#        minTmp = -1
#        index = -1
#        for k in range(1,n-i):     #for each possible number of flip
#            
#            mySum = 0
#            pTot = 0
#            for j in range(1,k+1):   #for each amelioration we can hope
#                p = probabilityGoodFlipLog10(n,k,j,i)
#                mySum += p * bestSoFar[i+j][0]
#                pTot += p
#            
#            mySum += 1  # We had the iteration
#            if pTot != 0:
#                mySum = mySum * (1/pTot) # We solve the equation
#                if mySum < minTmp or minTmp == -1:
#                    minTmp = mySum
#                    index = k
#        
#        #index = tmpList.index(min(tmpList))
#        bestSoFar[i] = (minTmp,index)
#    
#    return bestSoFar
#
#

table = np.load("tables/oneEA/1000.npy")
table = table.item()
del table['Expected Time General']
SIZE = len(table)
tabLog = np.cumsum(np.log10(np.arange(1,SIZE+1)))

x = list(range(SIZE,SIZE//2,-1))
y = [table[i][1] for i in table.keys()][:-SIZE//2]
#print(y)

def func(x,a,b):
    #print(x,a,b,c)
    return 1 / (a * x + b)

popt, pcov = opti.curve_fit(func,x,y)
#print(*popt)
plt.plot(x,y)
newLab = [func(x1, *popt) for x1 in x]
plt.plot(x, newLab, 'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
plt.legend()

##print(tabLog[1] - tabLog[0] - tabLog[0])
##print(tabLog)
##tabLog = np.cumsum(tabLog)
#opti = optimalOneMax(SIZE)
#print(opti)
#    
##prob = probabilityGoodFlipLog10(100,1,1,98)
##probAttendue = probabilityGoodFlip(100,1,1,98)
##print(tabLog)
##print(prob)
##print(probAttendue)

#print(table)
#mySum = 0
#for i in range(1,SIZE+1):
#    mySum += 10**(log10BinomCoef(SIZE,i) - SIZE * np.log10(2)) * table[i][0]
#print(mySum)

#table = np.load('tables/oneEA/1000.npy').item()
#table2 = [table[i][1] for i in table][:-500]
#print(table2)
#plt.plot(range(1000,499,-1),table2)

#mySum = 0
#diff = []
#l = []
#for i in range(SIZE//2+1,SIZE+1):
#    formula = 1 / (2 * i + 2 - SIZE)
#    l.append(formula)
#    diffTmp = table[i][1] - formula
#    diff.append(diffTmp)
##print(diff)
#plt.plot(range(1000,500,-1),l[::-1])

#mySum = 0
#for i in range(1,SIZE+1):
#    mySum += 10**(log10BinomCoef(SIZE,i) - SIZE * np.log10(2)) * bestSoFar[i][0]

        
#print(probabilityGoodFlipLog10(5,3,3,3))


#
#
#TABLE_COMP = "table500.npy"        # The table with optimal and "optimal" k to use
#NUMBER_OF_RUNS = 100  #The number of runs to do the mean
#
#def getRandomVector(size):
#    ''' Give a random vector of 0 and 1
#        size : the size of the vector '''
#        
#    return np.random.randint(2,size=size)


#def RLS_OneMax(table,size):
#    ''' apply the RLS algorithm on the OneMax problem and return the number of iteration to the goal.
#        table : The list that indicate wich number of bits you should flip at each stage
#    '''
#    
#    # We get the random vector
#    vector = getRandomVector(size)
#    while sum(vector) <= size/2:
#        vector = getRandomVector(size)
#    
#    counter = 0   # Our counter of steps
#    fitness = sum(vector)
#    
#    
#    # While we are not at the optimum
#    while fitness != size:
#        # Get the number of bits to flip
#        k = int(table[fitness - (size//2)-1])
#        to_flip = np.random.choice(size,k,replace=False)
#        #print(to_flip)
#        
#        # Flip them
#        offspring = copy.deepcopy(vector)
#
#        for i in to_flip:
#            offspring[i] = (offspring[i] + 1) % 2
#        
#        # Get the new fitness
#        fitnessOffspring = sum(offspring)
#        
#        # If it's better than before, we keep the offspring
#        if fitness < fitnessOffspring:
#            fitness = fitnessOffspring
#            vector = copy.deepcopy(offspring)
#        
#        #print(fitness)
#        #print(vector)
#        counter += 1
#    
#    return counter
#
## Load the comparative table
#tableComp = np.load(TABLE_COMP)
#size = len(tableComp) * 2
#
#results = [] # The list of results we'll get
#
#optimal = tableComp[:,0]    # optimal table
#non_opt = tableComp[:,1]    # "optimal" table
#static = np.ones(len(tableComp)) #static table
#
#lres = []
#for i in range(NUMBER_OF_RUNS):
#    res = RLS_OneMax(optimal,size)
#    lres.append(res)
#    print(res)
#    
#print("moyenne",sum(lres)/len(lres))

#tables = [static,non_opt,optimal]
#for i in range(0,len(tables)):
#    listeRes = [] # the list of resultat of each run
#    for j in range(NUMBER_OF_RUNS):
#        listeRes.append(RLS_OneMax(tables[i],size))
#        
#    results.append(sum(listeRes)/len(listeRes)) # We get the mean of all the runs
    
#print("Static mean : ", results[0])
#print("\"Optimal\" mean : ", results[1])
#print("optimal mean : ", results[2])
    

