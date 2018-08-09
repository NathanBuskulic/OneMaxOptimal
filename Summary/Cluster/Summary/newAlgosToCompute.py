#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 14:30:12 2018

@author: Nathan
"""

import subprocess as sp
#from multiprocessing import Process
from multiprocessing import Pool
import sys

SIZE = int(sys.argv[1])

python = "python3.5"

# We launch all the processes except the drift one
poolOne = Pool(processes = 4)
poolOne.apply_async(sp.call,([python,"old1+1Sup0.py",str(SIZE),str(SIZE) + "/old1+1Sup0-lowerBound",str(1/(2*SIZE))],))
poolOne.apply_async(sp.call,([python,"optimal1+1sup0.py",str(SIZE)+"/RLS-opt.npy",str(SIZE)+"/p-Sup0-opt-medBound",str(1/(2*SIZE))],))
poolOne.apply_async(sp.call,([python,"optimal1+1sup0.py",str(SIZE)+"/RLS-opt.npy",str(SIZE)+"/p-Sup0-opt-highBound",str(1/SIZE)],))
poolOne.apply_async(sp.call,([python,"optimalStaticP.py",str(SIZE),str(SIZE)+"/staticP-final.npy"],))

# We launch the first drift ones
poolDrift = Pool(processes = 2)
poolDrift.apply_async(sp.call,([python,"optimalEADriftSup0.py",str(SIZE)+"/full-drift.npy",str(SIZE)+"/p-Sup0-drift-medBound",str(1/(2*SIZE))],))
poolDrift.apply_async(sp.call,([python,"optimalEADriftSup0.py",str(SIZE)+"/full-drift.npy",str(SIZE)+"/p-Sup0-drift-highBound",str(1/SIZE)],))

# Waiting for the results
poolDrift.close()
poolDrift.join()

# Getting the final drift results
poolDrift = Pool(processes = 2)
poolDrift.apply_async(sp.call,([python,"getExpectedTimeEA.py",str(SIZE)+"/p-Sup0-drift-medBound.npy",str(SIZE)+"/p-Sup0-drift-medBound-2","True"],))
poolDrift.apply_async(sp.call,([python,"getExpectedTimeEA.py",str(SIZE)+"/p-Sup0-drift-highBound.npy",str(SIZE)+"/p-Sup0-drift-highBound-2","True"],))

#closing everything
poolOne.close()
poolDrift.close()
poolOne.join()
poolDrift.join()



#def oldSup0():
#    sp.call([python,"old1+1Sup0.py",str(SIZE),str(SIZE) + "/old1+1Sup0-lowerBound",str(1/(2*SIZE))])
# 
#def sup0ChangeBound():
#    sp.call([python,"old1+1Sup0.py",str(SIZE),str(SIZE) + "/old1+1Sup0-lowerBound",str(1/(2*SIZE))])
#    
#def pdrift():
#    sp.call([python,"optimalPDrift.py",str(SIZE)+"/full-drift.npy",str(SIZE)+"/p-drift"])
#    sp.call([python,"getExpectedTimeEA.py",str(SIZE)+"/p-drift.npy",str(SIZE)+"/p-drift-2"])
#    
#def optimal1Sup0():
#    sp.call([python,"optimal1+1sup0.py",str(SIZE)+"/RLS-opt.npy",str(SIZE)+"/p-Sup0-opt"])
#    
#def pdriftSup0():
#    sp.call([python,"optimalEADriftSup0.py",str(SIZE)+"/full-drift.npy",str(SIZE)+"/p-Sup0-drift"])
#    sp.call([python,"getExpectedTimeEA.py",str(SIZE)+"/p-Sup0-drift.npy",str(SIZE)+"/p-Sup0-drift-2","True"])
#    
#def baeck():
#    sp.call([python,"baeckEA.py",str(SIZE),str(SIZE)+"/baeck"])
#    
#def oldValues():
#    tabProc = []
#    tabProc.append(Process(target=sp.call,args=([python,"originalRLS.py",str(SIZE),str(SIZE) + "/oldRLS"],)))
#    tabProc.append(Process(target=sp.call,args=([python,"old1+1EA.py",str(SIZE),str(SIZE) + "/old1+1EA"],)))
#    tabProc.append(Process(target=sp.call,args=([python,"old1+1Sup0.py",str(SIZE),str(SIZE) + "/old1+1Sup0"],)))
#    
#    for i in range(len(tabProc)):
#        tabProc[i].start()
#    for i in range(len(tabProc)):
#        tabProc[i].join()
#        
#    
#if __name__ == '__main__':
#    # Initialise processus
#    driftProc = Process(target=drift)
#    pdriftProc = Process(target=pdrift)
#    optimal1Sup0Proc = Process(target=optimal1Sup0)
#    pdriftSup0Proc = Process(target=pdriftSup0)
#    baeckProc = Process(target=baeck)
#    oldValuesProc = Process(target=oldValues)
#    
#    # launch the one we can launch independantly
#    print("Launching baeck")
#    baeckProc.start()
#    print("Launching optimal1+1Sup0")
#    optimal1Sup0Proc.start()
#    print("Launching oldValues")
#    oldValuesProc.start()
#    
#    # Wait for the result of this guy
#    print("Launching drift")
#    driftProc.start()
#    driftProc.join()
#    
#    # Start the rest
#    print("Launching driftP")
#    pdriftProc.start()
#    print("Launching driftPSup0")
#    pdriftSup0Proc.start()
#    
#    #Close everyone
#    print("Closing everyone")
#    baeckProc.join()
#    optimal1Sup0Proc.join()
#    pdriftProc.join()
#    pdriftSup0Proc.join()
#    oldValuesProc.join()
#    print("end of the closing session")
