from math import cos as cosine
from typing import List

import numpy as np
from sympy import Expr, Rational, cos, diff, expand, factorial, floor, symbols

x, t, k, th = symbols("x t k θ")
gen_Legendre: Expr = (1 - 2 * x * t + t**2) ** Rational(-1, 2)


class LegendreStore:
    def __init__(self):
        self.reset()

    def reset(self, definition=True, recursion=True):
        # Stores differentiation of the generating function when using def
        if definition:
            self.definition: List[Expr] = [
                (1 - 2 * x * t + t**2) ** Rational(-1, 2),
                -Rational(1, 2)
                * (2 * t - 2 * x)
                * (1 - 2 * x * t + t**2) ** Rational(-3, 2),
            ]

        # Stores the Legendre polynomials when using recursion
        if recursion:
            self.recursion: List[Expr] = [x**0, x**1]


legendre_store = LegendreStore()


def legendre_def(n: int, eval: int | float | np.ndarray | None = None, store: bool = True):
    if n == 0:
        return (
            x**0
            if eval is None
            else (1.0 if isinstance(eval, (int, float)) else np.ones_like(eval))
        )
    elif n == 1:
        return x**1 if eval is None else eval
    else:
        pol: Expr
        if store:
            for i in range(len(legendre_store.definition), n + 1):
                legendre_store.definition.append(
                    diff(legendre_store.definition[i - 1], t, 1)
                )
            pol = expand(
                (1 / factorial(n)) * legendre_store.definition[n].subs(t, 0),
                deep=True,
                mul=True,
                multinomial=False,
                power_exp=False,
                power_base=False,
                log=False,
            )
        else:
            pol = expand(
                (1 / factorial(n)) * diff(gen_Legendre, t, n).subs(t, 0),
                deep=True,
                mul=True,
                multinomial=False,
                power_exp=False,
                power_base=False,
                log=False,
            )
    if eval is None:
        return pol
    else:
        if isinstance(eval, (int, float)):
            return float(pol.subs(x, eval))
        else:
            return np.vectorize(lambda val: float(pol.subs(x, val)))(eval)


def legendre_rec(n: int, eval: int | float | np.ndarray | None = None, store: bool = True):
    if n == 0:
        return (
            x**0
            if eval is None
            else (1.0 if isinstance(eval, (int, float)) else np.ones_like(eval))
        )
    elif n == 1:
        return x**1 if eval is None else eval
    else:
        if store:
            for i in range(len(legendre_store.recursion), n + 1):
                legendre_store.recursion.append(
                    expand(
                        (
                            (2 * i - 1) * x * legendre_store.recursion[i - 1]
                            - (i - 1) * legendre_store.recursion[i - 2]
                        )
                        / i,
                        deep=True,
                        mul=True,
                        multinomial=False,
                        power_exp=False,
                        power_base=False,
                        log=False,
                    ),
                )
            if eval is None:
                return legendre_store.recursion[n]
            else:
                if isinstance(eval, (int, float)):
                    return float(legendre_store.recursion[n].subs(x, eval))
                else:
                    return np.vectorize(
                        lambda val: float(legendre_store.recursion[n].subs(x, val))
                    )(eval)
        else:
            prev_pol, curr_pol = (
                (x**0, x**1)
                if eval is None
                else (legendre_rec(0, eval=eval), legendre_rec(1, eval=eval))
            )
            for i in range(2, n + 1):
                prev_pol, curr_pol = (
                    curr_pol,
                    (
                        expand(
                            ((2 * i - 1) * x * curr_pol - (i - 1) * prev_pol) / i,
                            deep=True,
                            mul=True,
                            multinomial=False,
                            power_exp=False,
                            power_base=False,
                            log=False,
                        )
                        if eval is None
                        else ((2 * i - 1) * eval * curr_pol - (i - 1) * prev_pol) / i
                    ),
                )
            return curr_pol


def legendre_exp(n: int, eval: int | float | np.ndarray | None = None):
    pol = (
        x * 0
        if eval is None
        else (0.0 if isinstance(eval, (int, float)) else np.zeros_like(eval))
    )
    for k in range(floor(n / 2) + 1):
        sum: Expr = (
            (1 if k % 2 == 0 else -1)
            * factorial(2 * n - 2 * k)
            / (2**n * factorial(k) * factorial(n - k) * factorial(n - 2 * k))
            * x ** (n - 2 * k)
        )
        if eval is None:
            pol += sum
        else:
            if isinstance(eval, (int, float)):
                pol += float(sum.subs(x, eval))
            else:
                pol += np.vectorize(lambda val: float(sum.subs(x, val)))(eval)
    return pol


def legendre(
    n: int, polar: bool = False, eval: int | float | np.ndarray | None = None
) -> Expr | float | np.ndarray:
    """
    Calculate the analytical expression of the Legendre polynomial.

    Args:
        n (int): The degree of the Legendre polynomial.
            Must be an integer greater than or equal to 0.
        polar (bool): If True, the function is returned in polar coordinates.
        eval (int, float, np.ndarray, None): The value(s) at which the polynomial is evaluated.
            If None, the polynomial is returned as an expression.
            Default is None.

    Returns:
        Expr: The Legendre polynomial of the given degree.

    Examples:
        ... code:: python

            >>> legendre(0)
            1
            >>> legendre(1)
            x
            >>> legendre(1, 0)
            0
    """  # noqa: E501
    try:
        n = int(n)
    except ValueError:
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be greater than or equal to 0")

    if eval is not None:
        if not isinstance(eval, (int, float)):
            try:
                eval = np.asarray(eval, dtype=float)
            except ValueError:
                raise TypeError("eval must be a number, an ndarray, or None")

    if eval is not None:
        if polar:
            eval = cosine(eval) if isinstance(eval, (int, float)) else np.cos(eval)
        return legendre_rec(n, eval=eval)
    else:
        return legendre_exp(n).subs(x, cos(th)) if polar else legendre_exp(n)
