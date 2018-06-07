#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 15:20:50 2018

@author: Nathan
"""

import numpy as np
import copy
import sys


TABLE_COMP = sys.argv[1]        # The table with optimal and "optimal" k to use
NUMBER_OF_RUNS = int(sys.argv[2])  #The number of runs to do the mean
PATH_TO_WRITE = sys.argv[3]

def getRandomVector(size):
    ''' Give a random vector of 0 and 1
        size : the size of the vector '''
        
    return np.random.randint(2,size=size)


def RLS_OneMax(table,size):
    ''' apply the RLS algorithm on the OneMax problem and return the number of iteration to the goal.
        table : The list that indicate wich number of bits you should flip at each stage
    '''
    
    # We get the random vector
    vector = getRandomVector(size)
    counter = 0   # Our counter of steps
    fitness = sum(vector)
    
    
    # While we are not at the optimum
    while fitness != size:
        # Get the number of bits to flip
        k = int(table[fitness][1])
        to_flip = np.random.choice(size,k,replace=False)
        
        # Flip them
        offspring = copy.deepcopy(vector)

        for i in to_flip:
            offspring[i] = (offspring[i] + 1) % 2
        
        # Get the new fitness
        fitnessOffspring = sum(offspring)
        
        # If it's better than before, we keep the offspring
        if fitness < fitnessOffspring:
            fitness = fitnessOffspring
            vector = copy.deepcopy(offspring)
        
        counter += 1
    
    return counter


def wilcoxon(l1,l2):
    ''' Compute the wicoxon rank sum test and return a boolean True if there is a statistical signification difference between the two lists
        l1, l2: the two lists you want to compare '''
    # We add the information of membership to the lists    
    l1 = [(i,'A') for i in l1]
    l2 = [(i,'B') for i in l2]
    l = l1 + l2
    l.sort(key=lambda tup:tup[0])
    
    # We calculate the total rank of l1
    rankl1 = 0
    for i in range(len(l)):
        if l[i][1] == 'A':
            rankl1 += i+1
    
    #We get l'esperance and the variance of the law will use
    E = len(l1) * (len(l1) + len(l2) + 1) / 2
    V = len(l1) * len(l2) * (len(l1) + len(l2) + 1) / 12
    
    # We get the result at a 5% threshold
    result = abs(rankl1 - E) / np.sqrt(V)
    print(result)
    return result > 1.96



# Load the comparative table
tableComp = np.load(TABLE_COMP).item()
size = len(tableComp)

# get the three table we'll use
static = {}
eduardo = {}
optimal = {}

for key in tableComp:
    static[key] = tableComp[key][0]
    eduardo[key] = tableComp[key][1]
    optimal[key] = tableComp[key][2]
    
    

resultsTmp = [] # The list of results we'll get

tables = [static,eduardo,optimal]
for i in range(0,len(tables)):
    listeRes = [] # the list of resultat of each run
    for j in range(NUMBER_OF_RUNS):
        listeRes.append(RLS_OneMax(tables[i],size))
        
    resultsTmp.append(listeRes) # We get all the runs in one place
    
print(resultsTmp[0])
result = {'mean':[np.mean(i) for i in resultsTmp],'variance':[np.var(i) for i in resultsTmp],'statistical diff with opt':[wilcoxon(i,resultsTmp[2]) for i in resultsTmp]}


np.save(PATH_TO_WRITE,result)

    
#print("Static mean : ", results[0])
#print("\"Optimal\" mean : ", results[1])
#print("optimal mean : ", results[2])

        
        
    