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

3 - (optional) Lower bound, if not provided takes 1/(n^2)

## dynamic (1+1)EA{>0}-p-drift
Compute the drift-maximizing parameters for a (1+1)EA{>0}.
First, launch optimalEADriftSup0.py file with parameters :

1 - Path to the data of RLS-drift

2 - Path to the file where you want to save the data

3 - (optional) Lower bound, if not provided takes 1/(n^2)

Then, launch getExpectedTimeEA.py with parameters:

1 - Path to the data you just computed

2 - Path to the file where you want to save the data

3 - (optional) Boolean to know if you want to use Bin{>0} or not. Use 'True' if you want in any other cases, it will use normal Bin(). (For that algorithm you want to set it to True)

## dynamic (1+1)EA-p-optimal
Compute the time-minimizing parameters for a (1+1)EA.
Launch optimal1+1EA.py file with parameters :

1 - Path to the data of RLS-opt

2 - Path to the file where you want to save the data

## dynamic (1+1)EA-p-drift

Compute the drift-maximizing parameters for a (1+1)EA.
First, launch optimalPDrift.py file with parameters :

1 - Path to the data of RLS-drift

2 - Path to the file where you want to save the data

Then, launch getExpectedTimeEA.py with parameters:

1 - Path to the data you just computed

2 - Path to the file where you want to save the data

3 - (optional) Boolean to know if you want to use Bin{>0} or not. Use 'True' if you want in any other cases, it will use normal Bin(). (For that algorithm you **do not** want to set it to True)

## dynamic (1+1)EA-Baëck
Compute the parameters and the expected time of a (1+1)EA using Baëck formula.
Launch baeckEA.py file with parameters :

1 - Size of the problem

2 - Path to the file where you want to save the data

## static RLS-1
Compute the parameters and the expected time of a RLS flipping always 1 bit.
Launch originalRLS.py file with parameters :

1 - Size of the problem

2 - Path to the file where you want to save the data

## static (1+1)EA-1/n
Compute the parameters and the expected time of a (1+1)EA{>0} using always p=1/n.
Launch old1+1EA.py file with parameters :

1 - Size of the problem

2 - Path to the file where you want to save the data

## static (1+1)EA{>0}-1/n

Compute the parameters and the expected time of a (1+1)EA{>0} using always p=1/n.
Launch old1+1Sup0.py file with parameters :

1 - Size of the problem

2 - Path to the file where you want to save the data

## static (1+1)EA-p-optimal
Compute the optimal static p and the expected time for a static (1+1)EA.
Launch optimalStaticP.py file with parameters :

1 - Size of the problem

2 - Path to the file where you want to save the data

# Get CSV files

In order to get the csv files associated with all of your data you can use one of the included file but it has a lot of restrictions. We encourage you to modify it to answer your needs (it's very simple)

## data on a single n-sized problem
To have the summary of every algorithms of a n-sized OneMax problem you can launch *createCSVSummary.py* :

1 - The path to a directory containing all of the 16 algorithms data file (in .npy) precisely named : RLS-opt, full-drift, p-Sup0-opt, p-Sup0-drift-2, EA-opt, p-drift-2, baeck, oldRLS, old1+1EA, old1+1Sup0, staticP-final, p-Sup0-drift-medBound-2, p-Sup0-drift-highBound-2, p-Sup0-opt-medBound, p-Sup0-opt-highBound, old1+1Sup0-lowerBound.

2 - The path where you want to save your .csv file (It's important to include the extension .csv in this parameter !)

## Summary table on every size
To have a summary on every problem size you can launch *createCSVExpectedTime.py*.
You need to launch the file in a directory where you have a directory for every size named by that size (a directory 100/, another one 500/ etc...).
In each one of these directories you need to have all the data file named as required in the single n-sized problem algorithm:

1 - The size where you want to stop. It will start at 100, then go to 500 up until the stop point by 500-size steps.

2 - The path where you want to save your .csv file.