from typing import Tuple

from sympy import Expr, I, Rational, Symbol, exp, factorial, pi

from .associated_legendre_functions import associated_legendre

PHI = Symbol("φ")


def spherical_harmonic(
    n: int,
    m: int,
    eval: Tuple[float, float] | None = None,
) -> Expr:
    """
    Calculate the analytical expression of the spherical harmonic

    Args:
        n (int): The subscript of the function.
            Must be an integer greater than or equal to 0.
        m (int): The superscript of the function.
            Must be an integer.
        eval Tuple[float, float] | None: The values (θ, φ) at which the function is evaluated.
            If None, the function is returned as an expression.
            Default is None.

    Returns:
        Expr: The spherical harmonic for the given subscript and superscript.

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
    if eval is not None:
        if not (isinstance(eval, tuple) or len(eval) == 2):
            raise ValueError("eval must be a tuple (θ, φ) of numbers or None")
        else:
            try:
                eval = tuple(float(x) for x in eval)
            except ValueError:
                raise ValueError("eval must be a tuple (θ, φ) of numbers.")

        th, phi = eval
        if m != 0 and (th == 0 or th == pi):
            return 0
        else:
            return (
                (1 if m % 2 == 0 else -1)
                * ((2 * n + 1) / (4 * pi) * factorial(n - m) / factorial(n + m))
                ** Rational(1 / 2)
                * associated_legendre(n, m, polar=True, eval=th)
                * exp(I * m * phi)
            )
    else:
        return (
            (1 if m % 2 == 0 else -1)
            * ((2 * n + 1) / (4 * pi) * factorial(n - m) / factorial(n + m))
            ** Rational(1 / 2)
            * associated_legendre(n, m, polar=True)
            * exp(I * m * PHI)
        )
