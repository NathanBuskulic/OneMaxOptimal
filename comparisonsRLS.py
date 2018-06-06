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
    while sum(vector) <= size/2:
        vector = getRandomVector(size)
    
    counter = 0   # Our counter of steps
    fitness = sum(vector)
    
    
    # While we are not at the optimum
    while fitness != size:
        # Get the number of bits to flip
        k = int(table[fitness - (size//2)-1])
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

# Load the comparative table
tableComp = np.load(TABLE_COMP)
size = len(tableComp) * 2

results = [] # The list of results we'll get

optimal = tableComp[:,0]    # optimal table
non_opt = tableComp[:,1]    # "optimal" table
static = np.ones(len(tableComp)) #static table

tables = [static,non_opt,optimal]
for i in range(0,len(tables)):
    listeRes = [] # the list of resultat of each run
    for j in range(NUMBER_OF_RUNS):
        listeRes.append(RLS_OneMax(tables[i],size))
        
    results.append(sum(listeRes)/len(listeRes)) # We get the mean of all the runs
    
print("Static mean : ", results[0])
print("\"Optimal\" mean : ", results[1])
print("optimal mean : ", results[2])

        
        
    