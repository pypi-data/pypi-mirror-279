from ..samples import Sample
import sympy as sp

def rvdict_to_samples(rvdict) -> list[Sample]:
    """Convert dict to a list of ``Sample`` objects

    Summary
    -------
    Random variables are initialised by passing ``Sample`` type objects.
    These form keys in the corresponding probability space. Conversions 
    from bare dicts to ``Sample`` objects are not built-in, so this helper 
    function aids in conversion

    Parameters
    ----------
    rvdict : dict
        keys are 'name' and 'pspace'

        - 'name' : sympy.Expr object, the name of the corresponding random variable
        - 'pspace' : dict, {'value': probability}. Note that ``probability`` is *not* used by this function in generating list of samples

    Returns
    -------
    samples : list[Sample]
        a list of ``Sample`` objects to be used in initialising a ``RandVar`` object

    Example
    -------
    >>> rv_name = sympy.Symbol('X') # more simply, can also have rv_name = 'X'
    >>> rvdict = {'name': rv_name, 'pspace': {'1.0': 0.5, '-1.0': 0.5}}
    >>> print(f'{*rv_dict_to_samples(rv_dict),}')
    ((X, 1.0), (X, -1.0))
        
    """
    name = rvdict['name'] # should be str or sp.Expr type object
    if isinstance(name, str):
        name = sp.Symbol(name) 

    pspace = rvdict['pspace']
    return [Sample(**{'name': name, 'value': float(v)}) for v in pspace.keys()]

def rvdict_to_pspace(rvdict) -> dict:
    """Convert dict to a probability space 

    Summary
    -------
    A continuation of the ``rvdict_to_samples()`` function, aimed at 
    converting a dict argument to probability space data in order to
    initialise a ``RandVar`` object (random variable)

    Parameters
    ----------
    rvdict : dict
        keys are 'name' and 'pspace'

        - 'name' : sympy.Expr object, the name of the corresponding random variable
        - 'pspace' : dict, {'value': probability}. Note that ``probability`` is *not* used by this function in generating list of samples
    
    Returns
    -------
    result : dict
        this is the probability space with ``Sample`` objects as keys and probabilities as values

    Example
    -------
    >>> rv_name = sympy.Symbol('X')
    >>> rvdict = {'name': rv_name, 'pspace': {'1.0': 0.5, '-1.0': 0.5}}
    >>> print(rv_dict_to_samples(rv_dict))
    {(X, 1.0): 0.5, (X, -1.0): 0.5}

    """
    rv_samples = rvdict_to_samples(rvdict)
    return dict(zip(rv_samples, rvdict['pspace'].values()))

def rvdict_to_init(rvdict) -> dict:
    """Convert bare dict arguments to RandVar init data

    Summary
    -------
    A continuation of ``rvdict_to_pspace``. Pass bare dict data which is easier to read and
    more intuitive, return a dict which can be used to initialise a ``RandVar`` object.

    Parameters
    ----------
    rvdict : dict
        bare dict defining a random variable, more intuitive and readable 

    Returns
    -------
    result : dict
        initialisation arguments for the ``RandVar`` class
    
    """
    pspace = rvdict_to_pspace(rvdict)
    name = next(psp.name for psp in pspace.keys())
    return {'name': name, 'pspace': pspace}
