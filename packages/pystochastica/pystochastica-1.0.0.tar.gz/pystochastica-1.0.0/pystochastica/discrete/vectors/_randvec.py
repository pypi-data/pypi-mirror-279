from ..core import JointDistribution
from ..variables import RandVar
from ..samples import Sample
from ..utils import generate_jdist
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import numpy as np
import sympy as sp

def sample_base_descent(*samplebases) -> tuple[Sample]:
    """Base conversion

    Summary
    -------
    Convert a list of ``SampleBase`` objects to ``Sample`` objects. This 
    allows for utilising the arithmentic encoded into the ``Sample`` class

    Parameters
    ----------
    samplebases : list[SampleBase] type
        a list of SampleBase type objects

    Returns
    -------
    samples : list[Sample]
        a list of Sample type objects
    
    """
    return tuple([Sample(name=samplebase.name, value=samplebase.value) for samplebase in samplebases])

def randvar_base_descent(*randvarbases) -> list[RandVar]:
    """Base conversion
    
    Summary
    -------
    Convert a list of ``RandVarBase`` objects to ``RandVar`` objects. This allows for 
    utilising the arithmetic coded into the ``RandVar`` class
    
    """
    return [RandVar(name=rv.name, pspace=rv.pspace) for rv in randvarbases]

class RandVec(JointDistribution):
    """
    
    Summary
    -------
    To model simultaneous and dependent random variables, use the ``RandVec`` class.
    The probability law for random vectors are joint distributions. In contrast to 
    stochastic processes, random vectors represent simultaneity of events. 

    Example
    -------
    For a random variable X, see that -X is dependent on X. If X is initialised as 
    a ``RandVar`` object, then we will typically find

    >>> bool((X-X).V == 0)
    False

    In order to correctly calculate X - X, we need to sum the ``RandVec`` object [X, -X]

    """
    def __init__(self, **joint_pspace: dict) -> None:
        super().__init__(**joint_pspace)

        # validate pspace keys are Sample type objects
        pspace_validated: dict = {
            sample_base_descent(*k): v for k, v in self.pspace.items()
        }
        self.pspace: dict = pspace_validated

        # generate random vector components
        self.derive_marginals()
        self.derive_secondaries()

        # Descent, RandvarBase --> RandVar, to fill random vector components
        self.components: np.ndarray = np.array(randvar_base_descent(*self.marginals))
        self.secondaries: np.ndarray = np.array(randvar_base_descent(*self.secondaries))

    def __add__(self, second_randvec):
        """Addition of ``RandVec`` objects

        Remarks
        -------

        The ``RandVec`` objects ``rvec1`` and ``rvec2`` are assumed to be *independent* as
        as random vectors. This means, for each component i, ``rvec1_i`` and ``rvec2_i`` are
        independent.

        - if ``rvec1`` and ``rvec2`` are dependent, initialise a new random vector with dependency in the joint distribution

        """
        if isinstance(second_randvec, (list, np.ndarray)): # pass list or np.ndarray with np.array.shape = (self.dimension,)
            try:
                second_randvec: list[Decimal] = [Decimal(str(v)) for v in second_randvec]
            except InvalidOperation:
                """second_randvec is a list of Fraction objects"""
                pass
            new_pspace: dict = {}
            for sample_tuple, prob in self.pspace.items():
                new_tuple = tuple([sample_tuple[i] + second_randvec[i] for i in range(self.dimension)])
                try:
                    new_pspace[new_tuple] += prob
                except KeyError:
                    new_pspace[new_tuple] = prob 
        else:
            new_marginals = [self.components[i] + second_randvec.components[i] for i in range(self.dimension)]
            new_pspace = generate_jdist(*new_marginals)
        
        return RandVec(pspace=new_pspace)

    def __radd__(self, second_randvec):
        return self.__add__(second_randvec)

    def __mul__(self, randvar):
        """Module structure

        Remarks
        -------
        Random vectors can be multiplied by scalars, random variables and functions thereof.
        If multiplying by random variables, note that they are assumed to be independent of 
        the components of the random vector. Current functionality in this method is 
        multiplication by:

        - ``int`` or ``float`` objects
        - ``RandVar`` objects

        """
        if isinstance(randvar, (int, float, Decimal, Fraction)):
            try:
                randvar: Decimal = Decimal(str(randvar))
            except InvalidOperation:
                # randvar is a Fraction object
                pass
            new_pspace: dict = {
                tuple([randvar*s for s in sample]): prob for sample, prob in self.pspace.items()
                }
        else:
            # randvar is a RandVar object
            new_pspace: dict = {}
            for rv_sample, rv_prob in randvar.pspace.items():
                for sample, prob in self.pspace.items():
                    new_tup = tuple([rv_sample*s for s in sample])
                    # new_tup = tuple([rv_sample] + list(sample))
                    new_prob = rv_prob*prob
                    try:
                        new_pspace[new_tup] += new_prob
                    except KeyError:
                        new_pspace[new_tup] = new_prob

        return RandVec(pspace=new_pspace)
    
    def __rmul__(self, randvar):
        return self.__mul__(randvar)

    def __sub__(self, second_rvec):
        second_rvec = (-1)*second_rvec
        return self.__add__(second_rvec)
    
    def __rsub__(self, second_rvec):
        neg_self = (-1)*self 
        return neg_self.__add__(second_rvec)
    
    def __neg__(self):
        return (-1)*self

    def dot(self, second_rvec):
        """
        Parameters
        ----------
        second_rvec : RandVec
            ``RandVec`` object to dot with self. Note, ``second_rvec`` is assumed to be
            independent of self

        Returns
        -------
        result : RandVar
            The dot product of two random vectors is a random variable
        
        """
        new_pspace: dict = {}
        if isinstance(second_rvec, (list, np.ndarray)):
            new_name = np.array([sample.name for sample in next(sample_tup for sample_tup in self.pspace.keys())])@second_rvec
            for sample_tup, prob in self.pspace.items():
                new_sample = np.array(sample_tup)@second_rvec
                try:
                    new_pspace[new_sample] += prob
                except KeyError:
                    new_pspace[new_sample] = prob
                    
            new_name = sp.nsimplify(new_name)
            return RandVar(**{'name': new_name, 'pspace': new_pspace})

        new_name = np.array([sample.name for sample in next(sample_tup for sample_tup in self.pspace.keys())])\
                    @ np.array([sample.name for sample in next(sample_tup for sample_tup in second_rvec.pspace.keys())])
        for sample_tup, prob in self.pspace.items():
            for second_sample_tup, second_prob in second_rvec.pspace.items():
                new_sample = np.array(sample_tup) @ np.array(second_sample_tup)
                new_prob = prob*second_prob
                try:
                    new_pspace[new_sample] += new_prob
                except KeyError:
                    new_pspace[new_sample] = new_prob

        new_name = sp.nsimplify(new_name)
        return RandVar(**{'name': new_name, 'pspace': new_pspace})
    
    def sum(self):
        """return the component sum of the random vector as a ``RandVar`` object (random variable)"""
        return self.dot(np.ones(self.dimension))

    def __matmul__(self, second_rvec):
        return self.dot(second_rvec)

    def calculate_expectation(self, inplace=False) -> None:
        expectation_vector = []
        for rv in self.components:
            if inplace == False:
                rv.calculate_expectation()
            else:
                expectation_vector += [rv.calculate_expectation(inplace=inplace)]
        
        if inplace == False:
            self.expectation: list[float] = [rv.expectation for rv in self.components]
        else:
            return expectation_vector
    
    @property
    def E(self):
        return np.array(self.calculate_expectation(inplace=True))

    def calculate_variance(self, inplace=False) -> None:
        components: np.ndarray = self.components
        secondaries: np.ndarray = self.secondaries

        cov_mtrx = np.full((self.dimension, self.dimension), np.nan)
        for i, component in enumerate(components):
            for j, second_component in enumerate(components[i:]): # components[i:] includes components[i]
                if j == 0:
                    cov_mtrx[i, i] = component.V
                else:
                    it = iter(secondaries)
                    secondary = next(s for s in it if s.name == component.name*second_component.name)
                    cov_mtrx[i, i+j] = secondary.E - component.E*second_component.E
                    cov_mtrx[i+j, i] = cov_mtrx[i, i+j]

        if inplace == False:
            self.cov_mtrx = cov_mtrx
        else:
            return cov_mtrx

    @property
    def V(self):
        return self.calculate_variance(inplace=True)

    def Prob(self, predicate: list[str]) -> float:
        """

        Parameters
        ----------
        predicate : str, list[str]
            the event whose probability is to be calculated (c.f., ``RandVar.Prov``)

        Returns
        -------
        probability : float
            the probability of the event passed. For the random vector [X, Y, Z, ...]
            and event ['<= x', '== y', '> z', ...], ``probability`` is the joint probability 
            Pr(X <= x, Y == y, Z > z, ...)

        Remarks
        -------
        
        Since random vectors represent simultaneity of events for the component random 
        variables, a list of events equal to the dimension of the random vector need to be passed (i.e., 
        ``len(predicate) == self.dimension``). If only a single event is passed, it is assumed to be 
        simultaneous across all random component random variables, e.g., passing '<= 1.0' returns the 
        probability Pr(X <= 1.0, Y <= 1.0, Z <= 1.0, ...)
        
        """
        if isinstance(predicate, str):
            return self.Prob([predicate]*self.dimension)

        rsult: Decimal = Decimal('0.0')
        for sample_tuple, prob in self.pspace.items():
            if all(eval(f"{sample_tuple[i].value}" + predicate[i]) for i in range(self.dimension)):
                try:
                    rsult += prob
                except TypeError:
                    rsult: float = float(rsult)
                    rsult += prob

        return rsult