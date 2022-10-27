# Biquaternionic-Matrices
A python package for the symbolic manipulation of biquaternionic valued 2 by 2 matrices.

A biquaternion (https://en.wikipedia.org/wiki/Biquaternion) is a quaternion Q = w + xI + yJ + zK (https://en.wikipedia.org/wiki/Quaternion) 
where the coefficients w,x,y,z are complex numbers  (and commute with I,J,K). 

During my 2021 research in Clifford algebras I found it necessary to run calculations with matrices of biquaternions, both symbolically and numerically.
While I could do these by hand, the noncommutative nature of the Biquaternions $\mathbb{B}$ would make these calculations difficult. 
So I decided to create some methods and a class to help me with these kinds of calculations.

Note: since this code heavilyuses  sympy, it is best implemented in Jupyter. I run my notebook in the same location as the package so I can quickly use 

from BiquaternionicMatrix import *


Goals:

-Matrix exponentiation

-Impliment larger matrices as an option?
