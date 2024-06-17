import sympy as sp
from decimal import Decimal, InvalidOperation
from fractions import Fraction

class SampleBase:

	def __new__(cls, **kwargs):
		"""Argument validation before calling the constructor method 
		
		Parameters
		----------
		name : sympy.Expr object
			The name assigned to the sample

		value : int, float, Decimal or Fraction type object
			The value assigned to the sample. 

			Note, `value` will be converted to a ``Decimal`` or ``Fraction`` type object.

		Raises
		------
		TypeError
			if name argument is not a ``sympy.Expr`` type object
			
			if value argument if not a ``float``, ``int``, ``Decimal`` or ``Fraction``

		Returns
		-------
		sample : SampleBase
			If erroneous arguments were passed, an error will be raised instead
		
		"""
		name = kwargs['name']
		value = kwargs['value']

		# type validations
		if not isinstance(name, sp.Expr):
			raise TypeError(f"{name} is not of type {sp.Expr.__name__}")
		
		if not isinstance(value, (int, float, Decimal, Fraction)):
			raise TypeError(f"{value} is not of type {int.__name__}, {float.__name__}, {Decimal.__name__} or {Fraction.__name__}")

		return super(SampleBase, cls).__new__(cls)

	def __init__(self, **kwargs) -> None:

		self.name: sp.Expr = kwargs['name']
		try:
			self.value: Decimal = Decimal(str(kwargs['value'])) # convert int or float type to Decimal
		except InvalidOperation: # value passed is a Fraction object, keep as raw
			self.value: Fraction = kwargs['value']

	# __eq__ and __hash__ ensures hashability of Sample objects
	def __eq__(self, second: object) -> bool:
		"""Test for when two ``SampleBase`` objects are equivalent
		
		Example
		-------
		>>> bool(Sample(name=sp.Symbol('X'), value=1.5) == Sample(name=sp.Symbol('Y'), value=1.5))
		False
		
		"""
		if not self.name == second.name:
			return False

		if not self.value == second.value:
			return False
		
		return True
	
	def __hash__(self) -> int:
		"""assign unique hash value to ``SampleBase`` object"""
		return hash(self.name) + hash(self.value)
	
	def __str__(self) -> str:
		"""``SampleBase`` objects are displayed on console by their name and value
		
		Example
		-------
		>>> print(SampleBase(name=sp.Symbol('X'), value=1.5))
		('X', 1.5)
		"""
		return f"{*(self.name, self.value),}"
