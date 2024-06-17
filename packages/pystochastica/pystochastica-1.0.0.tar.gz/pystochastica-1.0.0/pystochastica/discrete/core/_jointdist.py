from ._sample_base import SampleBase
from ._randvar_base import RandVarBase
from decimal import Decimal, InvalidOperation
import numpy as np

class JointDistribution:
    """

    Summary
    -------
    The distribution for random vectors are joint distributions. 
    Dependent random variables can also be modelled by joint distributions, 
    whence the dependent variables follow the marginal distributions of the joint
    distribution.

    Example
    -------
    X : random variable
        - X is dependent on X, whereby X - X = 0
        - if X is initialised as a randvar object, we would find X - X != 0
        - to get X - X == 0, form as RandVec operation [X, -X]@[1, 1] (c.f., discrete.vectors.RandVec)

    """
    def __new__(cls, **kwargs):
        """Argument validation before calling the constructor

        Parameters
        ----------
        pspace : dict type
            The joint probability distribution, constists of key-value pairs where:

            - the keys are ``tuple[SampleBase]`` type objects
            - the values are probabilities

        Raises
        ------
        TypeError
            if not all samples in pspace.keys() are SampleBase type objects

        ValueError
            if length of each tuple in pspace.keys() are not all equal

            if all probabilties do not sum to 1.0 (total law of probability)

        IndexError
            if name of all SampleBase objects at given index do not coincide

        Returns
        -------
        joint distribution : JointDistribution
            base object for the random vectors class (c.f., RandVec)

        """
        pspace: dict = kwargs['pspace']
        
        # validation of pspace keys, must be all of type Sample
        if not all(isinstance(sample, SampleBase) for sample_tuple in pspace.keys() for sample in sample_tuple):
            raise TypeError(f"not all samples in the probability space are of type {SampleBase.__name__}")
        
        # validation, each sample tuple must have the same length
        dimension = next(len(sample_tuple) for sample_tuple in pspace.keys())
        for sample_tuple in pspace.keys():
            if not len(sample_tuple) == dimension:
                raise ValueError(f"dimension mismatch, got {len(sample_tuple)}-dimensional for {sample_tuple} but expected {dimension}-dimensional")

        # validation, sample name at each index must coincide
        stacked = []
        for sample_tuple in pspace.keys():
            try:
                stacked = np.vstack([stacked, np.array([sample.name for sample in sample_tuple])])
            except ValueError:
                stacked = np.array([sample.name for sample in sample_tuple])

        if not all(len(set(stacked[:,i])) == 1 for i in range(dimension)):
            raise IndexError("sample index mismatch, all sample names at a given index must coincide")
        
        # validation, total law of probability
        try:
            all_probabilities: Decimal = sum([Decimal(str(p)) for p in pspace.values()])
        except InvalidOperation:
            # pspace.values() are Fraction objects
            all_probabilities: Decimal = Decimal(str(float(sum([p for p in pspace.values()]))))

        if not all_probabilities == Decimal('1.0'):
            raise ValueError(f"total law of probability violated, all probabilities must sum to {1.0} but got {all_probabilities}")

        return super(JointDistribution, cls).__new__(cls)

    def __init__(self, **kwargs) -> None:
        
        try:
            self.pspace: dict = {s: Decimal(str(p)) for s, p in kwargs['pspace'].items() if Decimal(str(p)) != Decimal('0')}
        except InvalidOperation:
            # kwargs['pspace'].values() are Fraction objects
            self.pspace: dict = kwargs['pspace']

        self.name: list = [sample.name for sample in next(s for s in self.pspace.keys())]
        self.dimension: int = next(len(sample_tuple) for sample_tuple in self.pspace.keys())

    def derive_marginals(self, inplace=False) -> None:
        """Generate marginal distributions from the joint distribution

        Example
        -------
        jd(X, Y, ...) : JointDistribution
            generate list of marginal distributions, [mX, mY, ...]
            
            - data of type ``list[RandVarBase]``
            - arguments of jd(X, Y, ...) are *not* RandVarBase objects

        Comment
        -------
        Random variables are marginals as derived from the joint distribution
        If random variables are passed individually to the constructor, they are independent

        - the prodict distribution is a joint distribution with independent marginals
        - i.e., if P(X, Y) = P(X)P(Y), then (X, Y) are independent

        """
        jdist_pspace: dict = self.pspace
        marginals: list = []
        for i in range(self.dimension):
            rv_name = next(sample for sample in jdist_pspace.keys())[i].name
            rv_pspace: dict = {}
            for sample_tuple, prob in jdist_pspace.items():
                sample: SampleBase = sample_tuple[i]
                try:
                    rv_pspace[sample] += prob
                except KeyError:
                    rv_pspace[sample] = prob

            marginals += [RandVarBase(**{'name': rv_name, 'pspace': rv_pspace})]

        if inplace == True:
            return marginals
        else:
            self.marginals: list[RandVarBase] = marginals

    @property
    def margs(self):
        return self.derive_marginals(inplace=True)

    def derive_secondaries(self, inplace=False) -> None:
        """Generate secondaries from joint distribution

        Example
        -------
        jd(X, Y, ...) : JointDistribution
            generate list[RandVarBase] object of secondaries

            - analogue of product distribution XY for X, Y independent
            - is generally *not* given by the product of marginals mXmY
            - marginals [mX, mY, ...] are assumed to be independent as ``RandVarBase`` objects

        """
        if self.dimension == 1:
            # return RandVarBase initialised for RandVar object
            secondary = RandVarBase(name=(next(sample.name for sample in self.pspace.keys())[0]), pspace=self.pspace)
            secondaries = [secondary]
            if inplace == True:
                return secondaries 
            else:
                self.secondaries = secondaries
                return
        
        jdist_pspace: dict = self.pspace
        secondaries: list = []
        for i in range(self.dimension-1):
            rv_i_name = next(sample for sample in jdist_pspace.keys())[i]
            for j in range(i+1, self.dimension):
                rv_j_name = next(sample for sample in jdist_pspace.keys())[j]

                rvrv_pspace: dict = {}
                name = rv_i_name.name*rv_j_name.name
                for sample_tuple, prob in jdist_pspace.items():
                    sample_name = name
                    sample_value = sample_tuple[i].value * sample_tuple[j].value
                    sample = SampleBase(name=sample_name, value=sample_value)
                    try:
                        rvrv_pspace[sample] += prob 
                    except KeyError:
                        rvrv_pspace[sample] = prob        

                secondaries += [RandVarBase(name=name, pspace=rvrv_pspace)]

        if inplace == True:
            return secondaries
        else:
            self.secondaries: list[RandVarBase] = secondaries

    @property
    def secnds(self):
        return self.derive_secondaries(inplace=True)

    def __str__(self) -> str:
        string: str = f"Joint Probability Distribution {*self.name,}"
        for sample_tuple, probability in self.pspace.items():
            string += "\n"
            for i, sample in enumerate(sample_tuple):
                if i != len(sample_tuple)-1:
                    string += f"{sample!s} AND "
                else:
                    string += f"{sample!s}"
            string += f"\t{probability = }"

        return string
    
    def to_tuple(self) -> tuple:
        """cast pspace to a tuple object, allows for hashing the pspace"""
        pspace: dict = self.pspace
        return tuple([(s, p) for s, p in pspace.items()])

    def __eq__(self, second_joint_dist: object) -> bool:

        if not set(self.name) == set(second_joint_dist):
            return False

        if not set(self.pspace.keys()) == set(second_joint_dist.pspace.keys()):
            return False
        
        for key, prob in self.pspace.items():
            if not second_joint_dist[key] == prob:
                return False
            
        return True

    def __hash__(self) -> int:
        return hash(self.to_tuple())
