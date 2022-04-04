# Advanced algorithms assignment
Advanced algorithms class assignment for A.A. year 2021/2022

## Assignment 1 - Minimum spanning tree
**Deadline: Monday 25 April, 11:55 pm**
## How to run cythonized code

 From the Lab1 directory where there is the setup.py file
 From a regular shell

	  python setup.py build_ext --inplace
	  python main.py 

Note that the cythonized files have a different name (they and in _compiled)
So the import from the main.py is changed accordingly
Main.py generates three .csv files containing the algorithms output.

After generating the .csv files, run:

    python plot.py

in order to gererate the final graphs.
