from cmath import exp as cexp
from math import factorial as fact
from math import pi as pi_num
from math import sqrt

import numpy as np
from sympy import Expr, I, Rational, Symbol, exp, factorial, pi

from .associated_legendre_functions import associated_legendre

PHI = Symbol("φ")


def spherical_harmonic(
    n: int,
    m: int,
    th: int | float | np.ndarray | None = None,
    phi: int | float | np.ndarray | None = None,
) -> Expr | float | complex | np.ndarray:
    """
    Calculate the analytical expression of the spherical harmonic.

    Args:
        n (int): The subscript of the function.
            Must be an integer greater than or equal to 0.
        m (int): The superscript of the function.
            Must be an integer.
        th (int, float, np.ndarray, None): The value(s) at which the function is evaluated.
            If None, the function is returned as an expression.
            Default is None.
        phi (int, float, np.ndarray, None): The value(s) at which the function is evaluated.
            If None, the function is returned as an expression.
            Default is None.

    Returns:
        Expr | float | complex | np.ndarray: The spherical harmonic for the given subscript and superscript.

    Examples:
        ... code:: python

            >>> spherical_harmonic(0, 0)
            1/sqrt(4*π)
            >>> spherical_harmonic(1, 0)
            sqrt(3)/sqrt(4*π)*cos(θ)
    """  # noqa: E501
    if not isinstance(n, int) or not isinstance(m, int):
        raise TypeError("n and m must both be integers")
    if n < 0:
        raise ValueError("n must be greater than or equal to 0")

    if (th is not None and phi is None) or (th is None and phi is not None):
        raise ValueError("th and phi must both be provided or both be None")

    if th is not None:
        coeff = sqrt((2 * n + 1) / (4 * pi_num) * fact(n - m) / fact(n + m))
        if not isinstance(th, (int, float)) or not isinstance(phi, (int, float)):
            try:
                th = np.asarray(th, dtype=float)
                phi = np.asarray(phi, dtype=float)
                if th.shape != phi.shape:
                    raise ValueError("th and phi must have the same shape")
            except ValueError:
                raise TypeError("th and phi must be numbers, arrays of numbers or None")
            return (
                coeff
                * associated_legendre(n, m, polar=True, eval=th)
                * np.exp(1j * m * phi)
            )
        else:
            return (
                coeff * associated_legendre(n, m, polar=True, eval=th) * cexp(1j * m * phi)
            )
    else:
        return (
            (
                ((2 * n + 1) / (4 * pi) * factorial(n - m) / factorial(n + m))
                ** Rational(1, 2)
            )
            * associated_legendre(n, m, polar=True)
            * exp(I * m * PHI)
        )
