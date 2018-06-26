#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 16:22:21 2018

@author: Nathan
"""

import numpy as np
import copy
    
class AdaptativePursuit:
    def __init__(self,n,pmin,alpha,beta,problem):
        self.n = n
        self.pmin = pmin
        self.pmax = 1 - (n-1)*self.pmin
        self.alpha = alpha
        self.beta = beta
        self.problem = problem
        
        # We initialise the lists of reward and probabilities
        self.probas = {}
        self.qualities = {}
        for i in range(1,self.n + 1):
            self.probas[i] = 1/self.n
            self.qualities[i] = 1.0
        
        print((copy.deepcopy(self.probas),self.problem.getState()))
        self.results = [(copy.deepcopy(self.probas),self.problem.getState())]
        
    def run(self):
        while not self.problem.isDone():
            # We choose an operator
            selectedOperator = np.random.choice(self.n,1,p=list(self.probas.values()))[0] + 1
            print(selectedOperator)
            
            # We get the associated reward
            reward = self.problem.step(selectedOperator)
            
            # We update our probabilities
            self.qualities[selectedOperator] += self.alpha * (reward - self.qualities[selectedOperator])
            astar = max(self.qualities.items(),key=lambda x:x[1])[0]
            self.probas[astar] += self.beta * (self.pmax - self.probas[astar])
            
            for i in range(1,self.n+1):
                if i != astar:
                    self.probas[i] += self.beta*(self.pmin - self.probas[i])
            
            self.results.append((copy.deepcopy(self.probas),self.problem.getState()))
            print((copy.deepcopy(self.probas),self.problem.getState()))
                
            
        def getResults(self):
            return self.results
        
        
class DynamicUCB:
    
    def __init__(self,delta,lamb,problem,scaling=2):
        
        self.delta = delta
        self.scaling = scaling
        self.lamb = lamb
        self.problem = problem
        self.nbTour = 0
        
        self.means = np.zeros(self.problem.size)
        self.ni = np.zeros(self.problem.size)
        self.mi = np.zeros(self.problem.size)
        self.maxMi = np.zeros(self.problem.size)
        
        self.results = []
        
        
    def run(self):
        while not self.problem.isDone():
            recompenses = []
            for i in range(len(self.ni)):
                if self.ni[i] == 0:
                    recompenses.append(i+1)
                else:
                    recompenses.append(self.means[i] + np.sqrt((self.scaling*np.log(sum(self.ni)))/self.ni[i]))
            #recompenses = [self.means[i] + np.sqrt((self.scaling*np.log(sum(self.ni)))/self.ni[i]) for i in range(self.problem.size) if self.ni[i] >0 else 0]
            self.results.append((copy.deepcopy(recompenses),self.problem.getState()))
            #print(copy.deepcopy(recompenses),self.problem.getState())
            
            maxRec = max(recompenses)
            maxInd = [i for i in range(len(recompenses)) if recompenses[i] == maxRec]
            #print(maxInd)
            selected_operator = int(np.random.choice(maxInd))
            reward = self.problem.step(selected_operator + 1)
            self.means[selected_operator] = 1/(self.ni[selected_operator] +1) * (self.ni[selected_operator] * self.means[selected_operator] + reward)
            self.ni[selected_operator] += 1
            self.mi[selected_operator] += (self.means[selected_operator] - reward + self.delta)
            self.maxMi[selected_operator] = max(self.mi[selected_operator],self.maxMi[selected_operator])
            
            if self.maxMi[selected_operator] - self.mi[selected_operator] > self.lamb:
                #print("YOUPI")
                self.means = np.zeros(self.problem.size)
                self.ni = np.zeros(self.problem.size)
                self.mi = np.zeros(self.problem.size)
                self.maxMi = np.zeros(self.problem.size)
            self.nbTour += 1
        
    def getResults(self):
        return self.results
                
class MutationChange:
    
    def __init__(self,A,B,p0,problem):
        self.A = A
        self.B = B
        self.p = p0
        self.problem = problem
        self.results = []
        
    def run(self):
        while not self.problem.isDone():
            k = 0
            while k == 0:
                k = np.random.binomial(self.problem.size,self.p)
            reward = self.problem.step(k)
            self.results.append((self.problem.getState(),self.p))
            if reward > 0:
                self.p = min(self.A * self.p,1/2)
            else:
                self.p = max(self.B*self.p,1/(self.problem.size ** 2))
                
            #self.results.append((self.p,self.problem))

    def getResults(self):
        return self.results           