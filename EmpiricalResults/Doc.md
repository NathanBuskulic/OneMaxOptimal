# Computation of empirical results on some algorithms

You will find here source code to compute empirical data on the behalf of the previously computed parameters to some algorithms.

## createSearchPoints.py
Compute a set of starting search points to be used across all your algorithm to reduce variance.
Launch the file with the following parameters :

1 - Size of the problem

2 - Number of runs you want

3 - Path to the file where you want to save the data

## getEmpiricalresults.py
Compute data to be used with the iohprofiler tool.
Launch the file with the following parameters :

1 - Path to the table with the parameter you want to use (computed in another section)

2 - Size of the problem (*could be calculated from the table...*)

3 - The number of run you want

4 - The name of your data (not the same thing as where to save them)

5 - The path to a directory containing a folder called *data_f1* where will be stored your data under a format understandable by the iohprofiler tool

6 - (optional, except if you want to use the next optional option) If set to 'True' compute your data using (1+1)EA, if anything else or nothing is provided, consider that you've gave RLS style data.

7 - (optional) The path to a table of starting search points computed previously. If nothing provided, will generate new searching points.
