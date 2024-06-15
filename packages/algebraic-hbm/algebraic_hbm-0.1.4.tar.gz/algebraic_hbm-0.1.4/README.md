# Algebraic Harmonic Balance Method

This package provides a Python implementation of the algebraic harmonic balance method (algebraic HBM) as proposed  by [[1](#reference-1)].

## Installation

The following command installs ```algebraic_hbm``` from the [Python Package Index](https://pypi.org/project/.../). You will need a working installation of ```Python>=3.10``` and ```pip```.

```sh
pip install algebraic-hbm
```

## Usage

### Computing a point on the frequency response curve

This example shows how to use the algebraic HBM framework to compute a point on the frequency response curve for a softening Duffing oscillator. First, the executable functions $`F_n`$ and $`\mathrm D F_n=(\frac{\mathrm d F_n}{\mathrm d \mathbf c}, \frac{\mathrm d F_n}{\mathrm d a})_n`$ (see [Theoretic background](###-theoretic-background)) are generated and then  $`F_n(\mathbf c; \Omega)=0`$ is solved via Newton's method as implemented in `scipy.optimize.fsolve`. This example can also be found [here](example_solve.py).

Required imports are:
```python
from algebraic_hbm import ODE_2nd_Order_Poly_Coeffs, Algebraic_HBM
```
In order to define a softening Duffing oscillator
```math
r(t,x) = x''(t) + 0.4 x'(t) - 0.4 x^3(t) - 0.3 \cos(\Omega t) = 0
```
we load a predefined example via
```python
softening_Duffing = ODE_2nd_Order_Poly_Coeffs.load_example(example="softening_Duffing")
```
This step is equivalent to the following:
```python
softening_Duffing = ODE_2nd_Order_Poly_Coeffs(mass=1, damping=.4, stiffness=1, excitation=(0,.3), monomials={3: -.4})
```
Then, initialize the algebraic HBM for the softening Duffing oscillator and ansatz order $`n \ge 1`$.
```python
n = 1
HBM = Algebraic_HBM(ODE=softening_Duffing, order=n)
```
Next, generate the multivariate polynomials that define the algebraic equation system $`F_n`$ as obtained from the algebraic HBM.
```python
HBM.generate_multivariate_polynomials()
```
Finally, compile the polynomials into excecutable functions $`F_n`$ and $`\mathrm DF_n`$.
```python
F, DF = HBM.compile()
```
The functions $`F_n`$ and $`\mathrm D F_n`$ can now be used to solve $`F_n(\mathbf c; \Omega)=0`$ via scipys Newton method where $`\Omega=1`$ (`a=1`) is a fixed excitation frequency and intial guess $`\mathbf c_{n,0} = 0`$ is set to zero.
```python
import numpy as np
from scipy.optimize import fsolve
c0, a = np.zeros(HBM.subspace_dim), 1.
c = fsolve(func=lambda x: F(x,a), fprime=lambda x: DF[0](x,a), x0=c0)
print(f"{c=}, norm(c)={np.linalg.norm(c):1.4f}")
```
The output should look something likes this:
```python
c=array(0., -0.2445, -0.6593]), norm(c)=0.7032
```
Here, `0.7032` is an approximation of the amplitude of the stationary periodic solution $`x_n`$ for $`n=1`$. In a similar way $`F_n`$ and $`\mathrm D F_n`$ may be used to perform a bifurcation analysis of the softening Duffing oscillator by computing an approximation of its frequency response as done here [[3](#reference-3)].

### Coefficient matrix for Macaulay framework

This example shows how to build the coefficient matrix of the algebraic representation (again, see [Theoretic background](###-theoretic-background)) that can be used in conjunction with the Macaulay matrix framework [[4](#reference-4)].  This example can also be found [here](example_coefficient_matrix.py).

Most of the steps are as in the above example, but instead of compiling executable functions we request the coefficient matrix at a given excitation frequency $`\Omega = 1`$ (`a=1`) by invoking ```HBM.get_monomial_coefficient_matrix```.
```python
from algebraic_hbm import softening_Duffing, Algebraic_HBM

n, a = 1, 1
HBM = Algebraic_HBM(ODE=softening_Duffing, order=n)
HBM.generate_multivariate_polynomials()
A = HBM.get_monomial_coefficient_matrix(a)
```
The output should look something likes this:
```python
A=array([[ 0. ,  0.4,  3. ,  0. ,  0. ],
       [ 0. ,  0.6,  1. ,  0. ,  2. ],
       [ 0. ,  0.6,  1. ,  2. ,  0. ],
       [ 0. ,  1. ,  1. ,  0. ,  0. ],
       [ 1. , -1. ,  0. ,  1. ,  0. ],
       [ 1. ,  0.3,  0. ,  0. ,  0. ],
       [ 1. ,  0.3,  0. ,  1. ,  2. ],
       [ 1. ,  0.3,  0. ,  3. ,  0. ],
       [ 1. ,  0.4,  0. ,  0. ,  1. ],
       [ 1. ,  1. ,  0. ,  1. ,  0. ],
       [ 1. ,  1.2,  2. ,  1. ,  0. ],
       [ 2. , -1. ,  0. ,  0. ,  1. ],
       [ 2. , -0.4,  0. ,  1. ,  0. ],
       [ 2. ,  0.3,  0. ,  0. ,  3. ],
       [ 2. ,  0.3,  0. ,  2. ,  1. ],
       [ 2. ,  1. ,  0. ,  0. ,  1. ],
       [ 2. ,  1.2,  2. ,  0. ,  1. ]])

```
Here, the values of the first column of `A` are the indices $`i`$ of the Fourier coefficient functions $`R_i(\mathbf c,\Omega)`$ and the remaining columns define the monomials $`b_{\mathbf w_i} \mathbf c_n^{\mathbf w_i}`$ where the second column of are the coefficients $`b_{\mathbf w_i}`$ and the remaining columns define the tuples $`\mathbf w_i`$. In this manner the matrix `A` may now be used as the coefficient matrix that defines a multivariate polynomial system as used in the Macaulay Matlab tool [MacaulayLab](https://gitlab.esat.kuleuven.be/Christof.Vermeersch/macaulaylab-public).

### Theoretic background

We are considering second order ordinary differential equations (ODEs) with polynomial coefficients in the state $`x : \mathbb T \subset \mathbb R \to \mathbb R`$, that is ODEs of the form
```math
r(t,x;u) = \rho x''(t) + \delta x'(t) + \sum_{i=1}^q \alpha_i x^i(t) - u(t) = 0 \,, \quad u(t) = \hat u \cos(\Omega t) \,.
```
The idea of the HBM is to yield approximations $`x_n(t) = c_0 + \sum_{i=1}^n c_{2i-1} \cos(i \Omega t) + c_{2i} \sin(i \Omega t)`$ of stationary periodic solutions $`x`$ of the ODE. Given a excitation frequency $`\Omega`$, the algebraic HBM of order $`n`$ yields a system of multivariate polynomials $`R_i`$, $`i=0,1,\ldots,2n`$, in the variables $`c_0,c_1,\ldots,c_{2n}`$ that solve the algebraic system
```math
F_n(\mathbf c; \Omega) = [R_i(\mathbf c; \Omega)]_{i=0}^{2n} = 0
```
where $`\mathbf c = [c_0,c_1,\ldots,c_{2n}] \in \mathbb R^{2n+1}`$. A solution $`\mathbf c \leftrightarrow x_n`$ of $`F_n(\mathbf c; \Omega) = 0`$ is also a solution of the (original) HBM defining system of integral equations
```math
\langle r(x_n), \phi_j\rangle = \frac{1}{T} \int_0^T r(t,x_n(t)) \phi_j(t) \, \mathrm d t \,, \quad j = 0,1,\ldots,2n \,,
```
with basis functions $`\phi_0(t) = 1`$, $`\phi_{2i-1}(t) = \cos(i \Omega t)`$ and $`\phi_{2i}(t) = \sin(i \Omega t)`$, $`i=1,\ldots,n`$. Note that building and evaluating $F_n$ does not require the computation of integrals as e.g. in the classical or Alternating Frequency-Time HBM [[2](#reference-2)].

## References

1. <a name="reference-1"></a>Hannes Dänschel and Lukas Lentz. "An Algebraic Representation of the Harmonic Balance Method for Ordinary Differential Equations with Polynomial Coefficients". Manuscript PDF: [/algebraic_hbm.pdf](/algebraic_hbm.pdf)
2. <a name="reference-2"></a>Malte Krack and Johann Gross. "Harmonic Balance for Nonlinear Vibration Problems". Springer, 2019. isbn: 978-3-030-14022-9. DOI: [10.1007/978-3-030-14023-6](https://doi.org/10.1007/978-3-030-14023-6)
3. <a name="reference-3"></a>Hannes Dänschel, Lukas Lentz, and Utz von Wagner. "Error Measures and Solution Artifacts of the Harmonic Balance Method on the Example of the Softening Duffing Oscillator". In: Journal of Theoretical and Applied Mechanics 62.2 (Apr. 2024), pp. 435–455. DOI: [10.15632/jtam-pl/186718](https://doi.org/10.15632/jtam-pl/186718)
4. <a name="reference-4"></a>Philippe Dreesen, Kim Batselier, and Bart De Moor. "Back to the Roots: Polynomial System Solving, Linear Algebra, Systems Theory". In: IFAC Proceedings Volumes 45.16 (2012), pp. 1203–1208. issn: 1474-6670. DOI: [10.3182/20120711-3-BE-2027.00217](https://doi.org/10.3182/20120711-3-BE-2027.00217)