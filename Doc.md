# Computation of optimal parameters for different EA algorithms on OneMax problem

You will find here a set of source code and the associated results in order to compute parameters to different algorithms to solve OneMax problem.
Below is a documentation on how to launch each one of this calculation on a Unix-based system. Since everything is in Python3, you will need to have *numpy* installed on your machine and possibly *scipy* for some of them.

Parameters are understood by the program in the order in wich you gave them, it's not very user friendly in some cases but it works for now. You need to separate each parameters by a space.

## dynamic RLS optimal
Compute the time-minimizing parameters for a dynamic RLS.
Launch the createOptimalTable.py file with parameters :
1 - Size of the problem
2 - Path to the file where you want to save the data

## dynamic RLS drift-maximizing
Compute the drift-maximizing parameters for a dynamic RLS.
First, launch the optimalEduardo.py file with parameters :
1 - Size of the problem
2 - Path to the file where you want to save the data

Then, launch getExpectedTimeEduardo.py with parameters :
1 - Path to the data you just compute in the first step
2 - Path to the file where you want to save the data

## dynamic (1+1)EA{>0}-p-optimal
Compute the time-minimizing parameters for a (1+1)EA{>0}.
Launch optimal1+1sup0.py file with parameters :
1 - Path to the data of RLS-opt
2 - Path to the file where you want to save the data
3 - (optional) Lower bound, if not provided take 1/(n^2)

## dynamic (1+1)EA{>0}-p-drift
Compute the drift-maximizing parameters for a (1+1)EA{>0}.
Launch optimal1+1sup0.py file with parameters :
1 - Path to the data of RLS-opt
2 - Path to the file where you want to save the data
3 - (optional) Lower bound, if not provided take 1/(n^2)

## dynamic (1+1)EA-p-optimal

## dynamic (1+1)EA-p-drift

## dynamic (1+1)EA-Baëck

## static RLS-1

## static (1+1)EA-1/n

## static (1+1)EA{>0}-1/n

## static (1+1)EA-p-optimal

##
