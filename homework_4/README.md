# Module numpy_challenge usage #
This module provides several functions to work with matrices using python3 numpy library.

**Please note** that if you run this module and not import it, there will appear four numpy arrays:
- fav_arr_1
- fav_arr_2
- fav_arr_3
- fav_arr_4

## This module provides the following **functions**: ##
- matrix_multiplication
- multiplication_check
- multiply_matrices
- compute_2d_distance
- compute_multidimensional_distance
- compute_pair_distances

## Module functions usage ##

### matrix_multiplication ##

Takes **two matrices** as two arguments and returns the result of their multiplication. **Please note that** if the dimensions of your matrices are not valid for multiplication you will get an ERROR message.

### multiplication_check ###

Takes a **list of matrices** and returns *True* if they can be multiplied in **corresponding order**, either way returns *False*.

### multiply_matrices ###

Takes a **list of matrices** and returns the result of their multiplication in the corresponding order if they can be multiplied, either way returns None.

### compute_2d_distance ###

Takes **two one-dimensional arrays with two values in each** and returns the **Euclidean distance** between them so as they would be the coorinates in two-dimensional space.

### compute_multidimensional_distance ###

Takes **two one-dimensional arrays with any number of values in them** and returns the **Euclidean distance** between them so as they would be the coorinates in multi-dimensional space. **Please note that** if you input non-one-dimensional arrays or if number of values in arrays is not equal, you will get an ERROR message.

### compute_pair_distances ###

Takes a matrix with observations in rows and features in columns and returns the matrix with **pair_distances** between all observations.

## Installation and usage ##

This script has been written and can be run on python3. Please note that in uses the **numpy library** so for correct script work you should upload into your virtual environment the *requirements.txt*.