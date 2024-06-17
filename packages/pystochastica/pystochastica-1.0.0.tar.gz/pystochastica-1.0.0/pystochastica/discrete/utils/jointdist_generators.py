from ..core import SampleBase
from itertools import product
from  functools import reduce
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import numpy as np
import sympy as sp

def list_product(array: list):
    """Big prod

    Parameters
    ----------
    array : list
        list of common objects with a ``__mul__`` method

    Returns
    -------
    result : object
        return the product of all elements in the list
        
    """
    return reduce(lambda x, y: x*y, array)

def generate_jdist(*marginals) -> dict:
    """The product distribution from a list of random variables

    Summary
    -------
    From a list of random variables (``RandVar`` objects), generate the 
    product distribution with given random variables as marginals (i.e., 
    the joint distribution for a list of independent random variables)

    Parameters
    ----------
    marginals : list[RandVar]
        a list of random variables, initialised as ``RandVar`` objects

    Returns
    -------
    result : dict
        the product distribution

    """
    sample_prob_pairs_list = []
    for mg_rv in marginals:
        try:
            sample_prob_pairs = [(sample, Decimal(str(prob))) for sample, prob in mg_rv.pspace.items()]
        except InvalidOperation:
            # probabilties are Fraction type objects, leave as such
            sample_prob_pairs = [(sample, prob) for sample, prob in mg_rv.pspace.items()]

        sample_prob_pairs_list += [sample_prob_pairs]

    sample_prob_pairs_all = product(*sample_prob_pairs_list)
    jd_pspace: dict = {}
    for sample_prob_pair in sample_prob_pairs_all:
        stacked = np.vstack(sample_prob_pair)
        jd_key = tuple(stacked[:,0])
        jd_value = list_product(stacked[:,1])
        try:
            jd_pspace[jd_key] += jd_value
        except KeyError:
            jd_pspace[jd_key] = jd_value

    return jd_pspace

def generate_jdist_random(\
        dimension: int = 3, 
        SAMPLE_SIZE_RANGE: tuple = (2, 6), 
        SAMPLE_VALUES: tuple = (-50, 50), 
        MIN: int = 1, 
        MAX: int = 100
        ) -> dict:
    """Random joint distribution

    Summary
    -------
    Generate parameters for a joint distribution at random.
    Marginals of this distribution are almost certainly dependent
    as random variables

    Parameters
    ----------
    dimension : int, optional
        the dimension of the random vector with this joint distribution, default is 3

    SAMPLE_SIZE_RANGE : tuple, optional
        the range of sample sizes for each marginal, default is (2, 6)

    SAMPLE_VALUES : tuple, optional
        the range of values each sample can take for each marginal, default is (-50, 50)

    MIN : int, optional
        required for generating probabilities
    
    MAX : int, optional
        required for generating probabilities

    Returns 
    -------
    result : dict
        the probability space for initialising a ``JointDistribution`` of ``RandVec`` object
    
    """
    sample_names: list = [sp.Symbol(f"X_{i}") for i in range(dimension)]
    samples: dict = {sample_name: [] for sample_name in sample_names}
    for sample_name in sample_names:
        num_samples: int = np.random.randint(*SAMPLE_SIZE_RANGE)
        for _ in range(num_samples):
            value = Decimal(str(np.random.uniform(*SAMPLE_VALUES)))
            sample_object = SampleBase(name=sample_name, value=value)
            samples[sample_name] += [sample_object]

    jd_samples: list = list(product(*list(samples.values())))
    jd_sample_size: int = len(jd_samples)
    probabilities_pre = [np.random.randint(MIN, MAX) for _ in range(jd_sample_size)]
    probabilities = [Fraction(pre, sum(probabilities_pre)) for pre in probabilities_pre]
    return dict(zip(jd_samples, probabilities))
