# Functional programming practice #

This function collection *functionap.py* provides several useful functions based of the principle of functional programming.

## Functions description ##

- **sequential_map** - takes any number of functions as positional arguments and a container with values as a last positional argument. This function returns a list of all container values after sequentional applying of functions to them.


- **consensus_filter** - takes any number of functions that return True or False as positional arguments and a container with values as a last positional argument. This function returns a list of values that passed all functions with True.


- **conditional_reduce** - takes two functions and a container with values as positional arguments. This function returns a single value which is the result of reduce apply of second function to the values that passed the condition of the first function.


- **func_chain** - takes any number of functions as positional arguments and returns a function concatenating them by sequential execution.


- **sequential_map_2** - realization of sequentional_map using func_chain. Takes any number of functions as positional arguments and a container with values as a last positional argument. This function returns a list of all container values after sequentional applying of functions to them.


- **single_partial** - takes one function and any named arguments and returns the partial function with arguments pre-set.


- **multiple_partial** - takes any number of functions and named arguments and returns the list of partial functions with arguments pre-set.


- **print_analogue** - print function complete analogue.


## Installation and usage ##

This script was written on Python 3.9 and is recommended to be run using Python 3.9 as well.