from ._sample_base import SampleBase
import sympy as sp
from decimal import Decimal, InvalidOperation

class RandVarBase:

	def __new__(cls, **kwargs):
		"""Argument validation before calling the constructor method

		Parameters
		----------
		name : sympy.Expr type
			name of the random variable
		pspace : dict type
			the probability law for this random variable, consists of key-value pairs:

			- the keys are ``SampleBase`` objects
			- the values are probabilities
		
		Raises
		------
		TypeError
			if sample name is not a ``sympy.Expr`` type object

			if sample is not a ``SampleBase`` type object

		NameError
			if sample name does not coincide with randvar name

		ValueError
			if probabilities are not values between (0, 1)
			
			if all probabilities do not sum to 1.0 (total law of probability)

		Returns
		-------
		randvarbase : RandVarBase
			base object for the random variables class (c.f., RandVar)
				
		"""
		# necessary keys to pass
		name = kwargs['name']
		pspace: dict = kwargs['pspace']

		# type validation for name
		if not isinstance(name, sp.Expr):
			raise TypeError(f"{name} is not a {sp.Expr.__name__} type object")

		# set validation, keys must be unique
		pspace_keys = pspace.keys()
		if not len(set(pspace_keys)) == len(pspace_keys):
			raise ValueError("not all samples are unique")

		# pspace validation, keys are Sample objects, values are probabilities
		for sample, probability in pspace.items():

			if not isinstance(sample, SampleBase):
				raise TypeError(f"{sample} is not a {SampleBase.__name__} type object")
			if not sample.name == name:
				raise NameError(f"{sample} erroneously assigned to {name}")
			
			probability_dec = Decimal(str(float(probability)))
			if not (Decimal('0') <= probability_dec and probability_dec <= Decimal('1')):
				raise ValueError(f"{probability} is not a valid probability")

		# validation, total law of probability
		try:
			all_probabilities: list[Decimal] = [Decimal(str(v)) for v in pspace.values()]
		except InvalidOperation:
			all_probabilities: list = list(pspace.values())

		total: Decimal = Decimal(str(float(sum(all_probabilities))))
		if not total == Decimal('1.0'):
			raise ValueError(f"total law of probability violated, got {total} but expected {1.0}")

		return super(RandVarBase, cls).__new__(cls)

	def __init__(self, **kwargs):
		"""Constructor method

		"""
		self.name: sp.Expr = kwargs['name']
		try:
			self.pspace: dict = {k: Decimal(str(v)) for k, v in kwargs['pspace'].items() if Decimal(str(v)) != Decimal('0')}
		except InvalidOperation:
			# kwargs['pspace'].values() are Fraction objects, leave as raw
			self.pspace: dict = kwargs['pspace']

	def to_tuple(self) -> tuple:
		"""cast pspace to a tuple object, allows for hashing the pspace
		
		Example
		-------
		>>> print(to_tuple({sample1: probability1, sample2: probability2}))
		((sample1, probability1), (sample2, probability2))
		
		"""
		pspace = self.pspace
		return tuple([(k, v) for k, v in pspace.items()])

	def __eq__(self, second_rv: object) -> bool:

		if not self.name == second_rv.name:
			return False

		if not self.to_tuple() == second_rv.to_tuple():
			return False
		
		return True

	def __hash__(self) -> int:
		"""assign unique hash value to ``RandVarBase`` object"""
		name = self.name 
		pspace_tuple: tuple = self.to_tuple()
		return hash(name) + hash(pspace_tuple)
	
	def __str__(self) -> str:
		"""RandVarBase objects are displayed on console by their name, samples and probabilties
		
		Example
		-------
		>>> X_name: sympy.Expr = sympy.Symbol('X')
		>>> X_pspace: dict = {SampleBase(name=X_name, value=-1): 0.3, SampleBase(name=X_name, value=1): 0.7}
		>>> X = RandVarBase(name=X_name, pspace=X_pspace)
		>>> print(X)
		Random variable X
		(X, -1) 	0.3
		(X, 1) 		0.7

		"""
		string: str = f"Random variable {self.name}"
		for sample, probability in self.pspace.items():
			string += f"\n{sample}\t{probability = }"

		return string
