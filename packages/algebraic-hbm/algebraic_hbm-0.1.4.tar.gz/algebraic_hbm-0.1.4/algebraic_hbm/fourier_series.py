from __future__ import annotations

# OS.
import sys

# Data types.
from dataclasses import dataclass, field
from collections.abc import Sequence
from numbers import Number
from fractions import Fraction

# Math.
import numpy as np

DEFAULT_COEFFICIENTS = (0.,)

@dataclass
class Fourier_Series():
	'''
	Class to represent a truncated Fourier series

		f(x) = c_0 + sum_{k=1}^n (c_{2k-1} cos(frequency*k*x) + c_{2k} sin(frequency*k*x))

	of order 'n'.

	Methods:
		- get_order: returns 'n'
		- get_fundamental_period: returns '2*pi/frequency/n'
		- derivative: returns the truncated Fourier series 'df/dx'
		- eval: evaluates 'f' at point of a given list or on '[0,T]' where 'T' is the fundamental period.
		- roots: computes the roots of 'f'
		- get_extrema: computes extrema of 'f'
		- get_max: computes the maximum of 'f'
		- get_max_abs: same as 'get_max()' but additionally takes the
		- get_rms: compute the root-mean-square of 'f'
	'''

	coefficients: Sequence = field(default_factory=lambda: DEFAULT_COEFFICIENTS)
	frequency:       float = None

	# Parameters for pretty printing.
	variable_name:              str = 't'
	frequency_name:             str = 'Ω' #'ω'
	print_dot_in_argument:     bool = True
	multiplication_symbol:      str = "*"
	print_coefficient_decimals: int = 4

	def __post_init__(self):

		# Make sure coefficients is a valid type.
		if not (isinstance(self.coefficients, Sequence) or isinstance(self.coefficients, np.ndarray)):
			raise TypeError(f"Expecting {Sequence.__name__} or {np.__name__ + '.' + np.ndarray.__name__}.")

		# Make sure coefficients is of type numpy.ndarray.
		if not isinstance(self.coefficients, np.ndarray):
			self.coefficients = np.array(self.coefficients)

		# We always want to keep the sine-cofficient, even if it is zero.
		if not self.coefficients.shape[0] % 2:
			self.coefficients = np.concatenate((self.coefficients, [0]))

	def __getitem__(self, item):
		return self.coefficients[item]

	def __setitem__(self, item, value):
		self.coefficients[int(item)] = value

	def __eq__(self, other):
		"""
		We want to be able to compare instances of this class. For the comparison
		we only consider the 'coefficients'- and 'frequency'-attribute
		"""

		# We only want to compare the coefficients and the frequency.
		coeffs = self.coefficients == other.coefficients
		if type(coeffs) is np.ndarray or issubclass(coeffs, Sequence):
			coeffs = all(coeffs)
		freqs = self.frequency == other.frequency
		
		return coeffs and freqs

	def __call__(self, T: Number | np.ndarray) -> Number | np.ndarray | tuple:
		"""
		Method that evaluates the function that is represented by an instance of this class."
		"""
		return self.eval(T)

	def get_order(self) -> int:
		"""
		Return the order of the Fourier series, that is return the number 'n' as in the class doc-string.
		"""
		n = int(self.coefficients.shape[0]/2)
		return n
	
	def get_dimension(self) -> int:
		"""
		Return the dimension of the real Fourier space this Fourier series lives in. That is, 
		returns the number '2n+1' where 'n' as in the class doc-string.
		"""
		return int(self.coefficients.shape[0])
	
	def get_fundamental_period(self) -> float:
		'''Returns the largest period of the Fourier series.'''
		return 2*np.pi/self.frequency/self.get_order()

	def derivative(self) -> Fourier_Series:
		'''Computes the derivative of the Fourier series by coefficient manipulation.'''

		# Get data.
		f = self.frequency
		c = self.coefficients
		m = c.shape[0]
		n = int(m/2)
		
		# We compute the derivative by going to the 2 x n matrix representation and computing A*c, 
		# where A is just skew-symmetric and c = [cosine coeffs, sine coeffs] is a 2 x n matrix.
		A = np.array([[0.,1.], [-1.,0.]])
		c_new = np.vstack((c[1::2]*np.arange(1,n+1), c[2::2]*np.arange(1,n+1))).reshape((2,n))
		c_new = np.reshape(np.transpose(A @ c_new), (2*n,))

		return Fourier_Series(coefficients=f*np.concatenate(([0], c_new)), frequency=f)

	def eval(self, T: Number | np.ndarray = None, no_evaluation_points: int = 10) -> Number | np.ndarray | tuple:
		'''Evaluates Fourier series at either every t in T or on the fundamental period.'''

		return_T = True
		if T is not None:
			return_T = False

		if not isinstance(T, Number) and type(T) not in [type(None), np.ndarray]:
			raise TypeError()

		if isinstance(T, Number):
			T = np.array([T])

		c = self.coefficients
		m = c.shape[0]
		n = int(m/2)
		f = self.frequency

		# (Quasi-) zero frequency.
		if f < sys.float_info.epsilon:
			T = np.array([0])

		# Generate evaluation points if needed.
		if T is None:
			T = np.linspace(0, 2*np.pi/f, m*no_evaluation_points)

		# If only constant harmonic given.
		if m == 1:

			# Get machine precision for datatype for comparison against zero.
			if np.issubdtype(c.dtype, np.integer):
				eps = 1
			elif np.issubdtype(c.dtype, np.floating):
				eps = np.finfo(c.dtype).eps
			else:
				raise TypeError()

			if np.abs(c[0]) < eps:
				Y = np.zeros(T.shape)
			else:
				Y = np.repeat(c[0], T.shape)

		else:
			# Now actually evaluate the Fourier series.
			Y = np.array([c[0] + sum(c[i]*np.cos(int(i/2+1)*f*t) if i%2 else c[i]*np.sin(int(i/2)*f*t) for i in range(1,m)) for t in T])

			if Y.shape == (1,):
				Y = Y[0]

		if return_T:
			return Y, T
		else:
			return Y

	def get_extrema(self) -> float:
		'''
		Compute extrema of the Fourier series (FS).

		That is, we compute the roots of the derivative of FS. The roots 
		are the angles of the eigenvalues of the Frobenius companion
		matrix of the trigonometric polynomial, i.e. the FS.
		'''

		if self.frequency == 0:
			return np.nan

		D     = self.derivative()
		roots = D.roots()

		return self.eval(roots)

	def get_max(self) -> float:
		'''Compute maximum of the Fourier series.'''

		if self.frequency == 0:
			return np.nan

		return np.max(self.get_extrema())

	def get_max_abs(self) -> float:
		'''Compute maximum of the Fourier series.'''

		if self.frequency == 0:
			return np.nan

		return np.max(np.abs(self.get_extrema()))
	
	#Todo: We should be able to numba-jit this routine.
	def frobenius(self) -> np.ndarray:
		"""
		Returns the Frobenius companion matrix associate with the series' coefficients.

		Adapted from eqs. (7),(9) of DOI:10.1007/s10665-006-9087-5.
		"""

		a = np.concatenate(([self.coefficients[0]],self.coefficients[1::2]))
		b = self.coefficients[2::2]
		N = int(self.coefficients.shape[0]/2)
		M = 2*N

		F = np.zeros((M,M), dtype=complex)
		for j in range(M):
			for k in range(M):

				if j==k-1:
					F[j,k] = 1

				elif j==M-1:
					if k == N:
						h = 2*a[0]
					if k < N:
						h = a[N-k] + 1j*b[N-k-1]
					else:
						h = a[k-N] - 1j*b[k-N-1]

					F[j,k] = -h/(a[-1] - 1j*b[-1])

		return F

	def roots(self) -> np.ndarray:
		'''Computes all roots of the Fourier series.'''

		# The real roots of the Fourier series are the real angles of the complex 
		# eigenvalues of the Frobenius companion matrix of the series coefficients.
		# 
		# According to eqs. (7),(9) of DOI:10.1007/s10665-006-9087-5.

		# Compute eigenvalues of Frobenius companion matrix.
		F = self.frobenius()

		# We can't have nans or infs in F.
		if not np.all(np.isfinite(F)):
			return np.array([np.nan])

		# Compute eigenvalues of F.
		z = np.linalg.eig(F)[0]

		# Compute and return roots by computing angles. We also have to transform
		# from (-pi,pi) to (-T/2, T/2) where T=2*pi/frequency.
		return np.angle(z)/self.frequency

	def get_rms(c) -> float:
		'''Computes the root-mean-square of the Fourier series.'''

		return np.sqrt(c[0]**2 + c[1:].dot(c[1:])/2)

	''' pretty printing '''

	def __str__(self) -> str:
		return self._pretty_repr()

	def pretty_print(self) -> str:
		print(self._pretty_repr())
	
	def _pretty_repr(self) -> str:
		"""
		repr-method that returns a formated string that represents this Fourier series as a
		sum of weighted trigonometric basis functions.
		"""

		if all(self.coefficients == 0):
			return str(0)

		s = ''
		k = 0

		# Iterate over each coefficient of the series.
		for c in self:

			# We can ignore all terms that have a zero-coefficient.
			if c == 0:
				k += 1
				continue
			
			# Take the absolute value since we print each coefficient 'c' manually.
			val = np.abs(c)

			# Properly format the leading sign symbol.
			if c > 0 and s != '':
				s += " + "
			elif c < 0 and s != '':
				s += " - "
			elif c < 0 and s == '':
				s += "-"

			
			# The first coefficient is always the once that has the constant basis function.
			# So we just print the coefficient and no basis function.
			if k == 0:
				s += self.pretty_constant(val)
				print(val)

			else:
				# Now we want to determin the index of and the basis function that we want to print.

				if k%2: # odd -> c*cos(k*x)
					j, operator = int((k-1)/2) + 1, "cos"

				else: # even -> c*sin(k*x)
					j, operator = int(k/2), "sin"
				
				# Concatenate everything. The pattern looks something like 'coefficient*cos(j*frequency*time)'.
				s += self.pretty_factor(val) + operator + "(" + self.pretty_argument(j,self.frequency) + ")"

			# Increments the index of the current coefficient.
			k += 1

		return s

	#Todo: Check if this method is still required.
	def get_angles(self):
		
		# Get cosine and sine coefficient indices.
		k = np.where(self.__array__() != 0)[0]
		cos = k[np.mod(k,2) == 1]
		sin = k[np.mod(k,2) == 0]

		# Computes frequencies based of cosine or sine coefficients.
		frequencies = np.zeros(self.__array__().shape)
		if np.any(cos):
			frequencies[cos] = (cos+1)/2

		if np.any(sin):
			frequencies[sin] = (sin+1)/2

		return self.frequency * frequencies

	def fractionate(self, z):
		"""
		Approximate number 'z' by a rational number and return information on it.
		"""

		# Get fraction representation.
		nom, denom = Fraction(z).as_integer_ratio()

		is_integer = False
		is_rational = False

		if denom == 1:
			is_integer = True
		else:
			is_integer = False
			is_rational = True

		return nom, denom, is_integer, is_rational

	#Todo: improve implementation: what if nom and denom are huge -> ugly -> make pretty
	def pretty_constant(self, z):
		"""
		Formats number 'a' in a pretty way.
		"""

		# Approximate 'z' as a rational number.
		nom, _, is_integer, is_rational = self.fractionate(z)

		# Straight forward formating if 'z' is integer.
		if is_integer:
			return str(nom)
		else:
			if is_rational:
				# Pretty format the ration number.
				return self.pretty_rational(z)
			else:
				#Todo: Is this case relevant, can it occur? Deprecated?
				raise NotImplementedError()

	#Todo: improve implementation: what if nom and denom are huge -> ugly -> make pretty
	def pretty_argument(self, j, f):
		"""
		Pretty format the argument 'a' of either cos(a) or sin(a).
		"""

		harmonic_index  = ""
		frequency = self.frequency_name
		variable  = self.variable_name
		mul_symbol_1 = self.multiplication_symbol
		mul_symbol_2 = self.multiplication_symbol

		# Prepare harmonic string.
		if j == 1:
			# We dont print the one.
			harmonic_index = ""
		elif j == -1:
			harmonic_index = "-"
		else:
			harmonic_index = str(j)

		# Format frequency.
		if f is not None:
			# f is given as a number.

			nom, _, is_integer, is_rational = self.fractionate(f)

			if is_integer:
				
				if nom == 1:
					frequency = ""
				elif nom == -1:
					raise NotImplementedError("Negative frequencies not yet implemented.")
				else:
					frequency = str(nom)

			else:

				if is_rational:
					frequency = self.pretty_rational(f)
				else:
					raise NotImplementedError()
		else:
			# f is not given so we treat it as being one so we dont print it.
			frequency = ""

		if harmonic_index == "":
			mul_symbol_1 = ""
		if frequency == "":
			mul_symbol_2 = ""

		return harmonic_index + mul_symbol_1 + frequency + mul_symbol_2 + variable

	#TODO: finish implementation: what if nom and denom are huge -> ugly -> make pretty
	def pretty_factor(self, z):
		"""
		Return formated coefficient/weight 'a' that is multiplied by the basis functions.
		"""

		# Approximate 'z' by rational number.
		nom, denom, is_integer, is_rational = self.fractionate(z)

		if is_integer:
			# Treat the integer case differently.			
			if nom == 1:
				return ""
			if nom == -1:
				return "-"
			else:
				return str(nom) + self.multiplication_symbol

		else:

			if is_rational and np.log10(nom) <= 4 and np.log10(denom) <= 4:
				# If the nominator is not too large we print 'z' as a rational number.
				fac = self.pretty_rational(z)
			else:
				# Print it as a floating point number with given number of decimals.
				fac = f"{z:1.{self.print_coefficient_decimals}f}"

				# Now remove trailing zeros after the period.
				while True:
					if fac[-1] == "0":
						fac = fac[:-1]
					else:
						break

			return fac + self.multiplication_symbol

	def pretty_rational(self, z):
		"""
		Pretty format the rational number 'z'.
		"""

		nom, denom = Fraction(z).as_integer_ratio()
		tol = 1e3
		if nom > tol:
			# Just format as this if the nominator is too large.
			s = f"{z:1.2f}"
		else:
			# Print a rational number.
			s = str(nom) + "/" + str(denom) 

		return s