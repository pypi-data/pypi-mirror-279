from itertools import product
import numpy as np

def dict_mul(*dicts) -> dict:
    """
    
    Summary
    -------
    Multiply arbitrary many dictionaries with key, value pairs being objects
    with a __mul__ method (i.e., can be multiplied). Return a dictionary of 
    the same type as the inputs

    Parameters
    ----------
    dictionaries : list[dict]
        the keys and values of any passed dictionary must be float type objects

    Returns
    -------
    dictionary : dict
        the keys and values will be float type objects
    
    Example
    -------
    >>> dict_1 = {1 : 0.3, 1.5: 0.7}
    >>> dict_2 = {10: 1.0}
    >>> dict_mul(dict_1, dict_2)
    {10: 0.3, 15: 0.7}  

    """
    key_value_pairs = product(*[d.items() for d in dicts])
    multiplied: dict = {}
    for key_values in key_value_pairs:
        stacked = np.vstack(key_values)
        key = np.prod(stacked[:,0])
        prob = np.prod(stacked[:,1])

        try:
            multiplied[key] += prob 
        except KeyError:
            multiplied[key] = prob 
            
    return multiplied
