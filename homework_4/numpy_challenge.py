import numpy as np


if __name__ == "__main__":
    """ here I created 4 np.arrays using 4 different methods just for training"""

    fav_list = [196, 295, 394, 493]
    fav_arr_1 = np.array(fav_list) # converted list to array

    fav_arr_2 = np.zeros(5) # array with zeros

    fav_arr_3 = np.arange(36, 46, 4) # like range, 4 is a step

    fav_arr_4 = np.linspace(1, 10, 5) # like range, but 5 is the number of values
    

def matrix_multiplication(mtr_1, mtr_2):
    """for two matrices multiplication if they can me multiplied in the original order"""

    if np.shape(mtr_1)[1] == np.shape(mtr_2)[0]: # check that matrices can be multiplied
        return np.matmul(mtr_1, mtr_2)

    else:
        return "ERROR: you have input two matrixes that can not be multiplied. Please check their "


def multiplication_check(matrices):
    """to check whether matrices from a list can be multiplied in the original order, output True or False"""

    res = True # flag that we hope would not change :)

    prev = np.shape(matrices[0]) # shape of the previous matrix
    for i in range(1, len(matrices)):
        curr = np.shape(matrices[i]) # shape of the current matrix
        if prev[1] != curr[0]:
            res = False # oh no flag changed, operation non valid
            break
        else:
            prev = (prev[0], curr[1]) # multiplied matrix shape

    return res
    

def multiply_matrices(matrices):
    """multiply several matrices in the original order if possible, either way return None"""

    res = matrices[0] # previous matrix

    for i in range(1, len(matrices)):
        curr = matrices[i] # current matrix
        if np.shape(res)[1] != np.shape(curr)[0]: # if matrices dimensions are not compatible
            return None

        res = np.matmul(res, curr) # if dimensions are ok, multiply

    return res


def compute_2d_distance(arr_1, arr_2):
    """takes two one-dimensional arrays with two values and computes the distance between them"""

    x_1, y_1 = arr_1[0], arr_1[1]
    x_2, y_2 = arr_2[0], arr_2[1]

    return np.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)


def compute_multidimensional_distance(arr_1, arr_2):
    """takes two one-dimensional arrays with any number of values and computes the distance between them"""

    if len(np.shape(arr_1)) != 1 or len(np.shape(arr_2)) != 1: # check for one-dimensional arrays
        return "ERROR: at least one of the arrays has more dimensions than one"

    if np.shape(arr_1)[0] != np.shape(arr_2)[0]: # check for correspondence of value numbers in both arrays
        return "ERROR: two arrays have different lengths"

    return np.sqrt(np.sum(np.square(arr_1 - arr_2)))


def compute_pair_distances(arr):
    """takes two two-dimensional arrays and returns pair distances matrix"""

    num_observations = len(arr) # how many observations

    res = np.zeros((num_observations, num_observations)) # yet empty matrix for results

    for i in range(num_observations):
        obs_i = arr[i]

        for j in range(i + 1, num_observations):
            obs_j = arr[j]

            i_j_dist = compute_multidimensional_distance(obs_i, obs_j) # distances for all combinations

            res[i][j] = i_j_dist
            res[j][i] = i_j_dist

    return res