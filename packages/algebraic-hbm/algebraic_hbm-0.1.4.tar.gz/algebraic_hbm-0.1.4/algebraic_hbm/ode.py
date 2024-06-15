from __future__ import annotations
from dataclasses import dataclass

from algebraic_hbm.fourier_series import Fourier_Series

@dataclass
class ODE_2nd_Order_Poly_Coeffs():
	"""
	Class representing a second order ODE with polynomial coefficients in x

	  mass*x'' + damping*x' + stiffness*x + f(x) = excitation
	
	where

	  f(x) = sum_i monomials[i]*x^i

	is a univariate-polynomial in x. The coefficients are:

	mass:       (linear) mass coefficient [real float]
	damping:    (linear) damping coefficient [real float]
	stiffness:  (linear) stiffness coefficient [real float]
	monomials:  dictonary with (key,value) pairs (i,coefficient[i]) such that 'monomial=monomials[i]*x**i'
	excitation: input/excitation - given as a <tuple> or <Fourier_Series> instance
	"""
	
	mass: float = None
	damping: float = None
	stiffness: float = None
	monomials: dict = None
	excitation: tuple | Fourier_Series = None

	# pretty_print options:
	symbol_state:          str = "x"
	symbol_time:           str = "t"
	multiplication_symbol: str = "*"
	print_time_argument:  bool = True

	def __post_init__(self):

		# Cast the excitation tuple to a Fourier_Series-instance.
		if type(self.excitation) is tuple:
			self.excitation = Fourier_Series(self.excitation)

		if self.monomials is None:
			self.monomials = {}

	@classmethod
	def load_example(cls, example: str="softening_Duffing"):
		"""
		Load predefined examples, e.g. a softening softening Duffing oscillator
		via 'load_example_ode(example="softening_Duffing")'.
		"""

		if type(example) != str:
			raise TypeError("'example' must be of type 'str'.")
		
		match example:
			case "softening_Duffing":
				return cls._load_example_softening_Duffing()

			case _:
				raise ValueError("Unknown example.")
				
	@classmethod
	def _load_example_softening_Duffing(cls):
		"""
		Define and load an instance that represents a softening Duffing oscillator.
		"""
		
		obj = cls()
		obj.mass = 1.
		obj.damping = .4
		obj.stiffness = 1.
		obj.monomials = {3: -.4}
		obj.excitation = Fourier_Series((0,.3))

		return obj

	def get_stationary_system(self) -> list:
		"""
		Returns a the stationary system as a list 'coeffs' of polynomial coefficients where

		  coeffs[0]*x^n + coeffs[1]*x^{n-1} + coeffs[2]*x^{n-2} + ... coeffs[n-1]*x + coeffs[n] = 0.
		"""
		self.excitation.frequency = 0
		coeffs = [-self.excitation(0), self.stiffness]
		last_i = 1
		for i in self.monomials:
			if i > last_i + 1:
				coeffs += [0.]*(i-1 - last_i) # Fill up w/ teros
			coeffs += [self.monomials[i]]
			last_i = i

		return coeffs[::-1]

	""" Pretty printing """

	def __str__(self) -> str:
		return self._pretty_repr()

	def pretty_print(self) -> str:
		print(self._pretty_repr())
	
	def _pretty_repr(self) -> str:
		"""
		repr-method that returns a formated string that represents a second order ordinary differential
		equation with polynomial coefficients.
		"""

		# Get string representing 2nd time derivative (ddx).
		s = self._pretty_repr_ddx()

		# Append remaing strings representing ODE, except for excitation string.
		for r in (self._pretty_repr_dx(), self._pretty_repr_x()):
			s += r

		# Append string representing excitation.
		ex = self._pretty_repr_excitation()
		if ex == "":
			s += "=0"
		else:
			s += "=" + ex

		# Insert spaces around +/- symbols.
		s = self._insert_spaces_around_pm_eq(s)

		return s
	
	def _pretty_repr_ddx(self) -> str:
		"""
		repr-method that returns a formated string that represents the 2nd derivative.
		"""

		if self.mass == 0:
			return ""
		
		if self.print_time_argument:
			time_argument = "(" + self.symbol_time + ")"
		else:
			time_argument = ""

		return self._format_number(self.mass) + "dd" + self.symbol_state + time_argument
	
	def _pretty_repr_dx(self) -> str:
		"""
		repr-method that returns a formated string that represents the 1st derivative.
		"""

		if not self.damping:
			return ""
		
		if self.print_time_argument:
			time_argument = "(" + self.symbol_time + ")"
		else:
			time_argument = ""

		return self._format_number(self.damping) + "d" + self.symbol_state + time_argument
		
	def _pretty_repr_x(self) -> str:
		"""
		repr-method that returns a formated string that represents the linear monomial 'coefficient*x'
		"""

		if self.monomials is None:
			return ""

		if self.print_time_argument:
			time_argument = "(" + self.symbol_time + ")"
		else:
			time_argument = ""

		s = ""
		if self.stiffness:
			s += self._format_number(self.stiffness) + self.symbol_state + time_argument

		for i in sorted(self.monomials):
			if self.monomials[i] == 0:
				continue

			# Make sure the power is formated nicely.
			power = "^" + str(i)

			# Append coefficient, state symbol, power and time argument.
			s += self._format_number(self.monomials[i]) + self.symbol_state + power + time_argument

		return s

	def _pretty_repr_excitation(self) -> str:
		"""
		repr-method that returns a formated string that represents the excitation/right-hand-side/input.
		"""
		
		if self.excitation is None:
			return ""
		
		return self.excitation._pretty_repr()

	def _format_number(self, z) -> str:
		"""
		Method that returns a formated string of the number 'z' that has the
		'self.multiplication_symbol' appended.
		"""

		if z == 1:
			return "+"
		
		elif z == -1:
			return "-"
		
		else:
			s = ""
			if z > 0:
				s += "+"
			else:
				s += "-"
			s += str(abs(z)) + self.multiplication_symbol
			return s

	def _insert_spaces_around_pm_eq(self, s: str) -> str:
		"""
		Adds whitespace around every "+" and "-" character in 's'.
		"""

		# Remove leading "+".
		if s[0] == "+":
			s = s[1:]

		# Do it for the total string.
		s = s.replace("+", " + ").replace("-", " - ").replace("=", " = ")

		# Now make sure the first term looks pretty.
		if s[:3] == " - ":
			s = s[1:]

		return s
	
#Deprecated: This will be removed in a future release.
softening_Duffing = ODE_2nd_Order_Poly_Coeffs(mass=1, damping=.4, stiffness=1, excitation=(0,.3), monomials={3: -.4})