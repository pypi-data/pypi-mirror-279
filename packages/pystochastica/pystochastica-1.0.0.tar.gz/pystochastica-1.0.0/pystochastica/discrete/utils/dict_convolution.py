from itertools import product
import numpy as np

def depr_convolve_dicts(first_dict: dict, second_dict: dict) -> dict:
    """this function is deprecated, see ``convolve_dicts`` below"""
    convolved_dict: dict = {}
    for key, val in first_dict.items():
        for key2, val2 in second_dict.items():
            try:
                convolved_dict[key + key2] += val*val2 
            except KeyError:
                convolved_dict[key + key2] = val*val2
    return convolved_dict

def convolve_dicts(first_dict: dict, second_dict: dict) -> dict:
    """Convolution of dictionaries

    Summary
    -------
    this function returns the convolution of dictionaries wih arbitrary values
    (either integral or rational) as keys. It coincides with the numpy.convolve 
    function if these keys are ordered, natural numbers. 

    Parameters
    ----------
    first_dict : dict
        first dictionary in the convolution

    second_dict : dict
        second dictionary in the convolution. Note, convolution is commutative,
        so the it doesn't matter which dictionary is first or second

    Returns
    -------
    convolved : dict
        the convolution of first_dict and second_dict

    Example
    -------
    >>> dict_1 = {0: 10, 1: 15, 2: 20}
    >>> dict_2 = {0: -1, 1: 0, 2: 1, 3: 2}
    >>> convolved = convolve_dicts(dict_1, dict_2)
    >>> numpy_convolved = numpy.convolve(dict_1.values(), dict_2.values())
    >>> print(bool(convolved == numpy_convolved))
    True

    >>> dict_1 = {-4: 10, -2.2: 15, 5: 20}
    >>> dict_2 = {0.01: -1, 100: 0, 2: 1, 5: 2}
    >>> convolved = convolve_dicts(dict_1, dict_2)
    >>> numpy_convolved = numpy.convolve(dict_1.values(), dict_2.values())
    >>> print(bool(convolved == numpy_convolved))
    False

    """
    key_value_pairs = product(first_dict.items(), second_dict.items())
    convolved: dict = {}
    for (k1, v1), (k2, v2) in key_value_pairs:
        try:
            convolved[k1 + k2] += v1*v2
        except KeyError:
            convolved[k1 + k2] = v1*v2

    return convolved

def convolve_dicts_many(*dicts) -> dict:
    """like ``convolve_dicts``, but now for arbitrary many dicts
    
    """
    key_value_pairs = product(*[d.items() for d in dicts])
    convolved: dict = {}
    for key_values in key_value_pairs:
        stacked = np.vstack(key_values)
        key = np.sum(stacked[:,0]) 
        value = np.prod(stacked[:,1])
        try:
            convolved[key] += value
        except KeyError:
            convolved[key] = value 

    return convolved

