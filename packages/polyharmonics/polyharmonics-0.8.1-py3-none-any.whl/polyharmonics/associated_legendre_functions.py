from math import cos as cosine
from math import factorial as fact
from math import pow, sqrt
from typing import Dict, List

import numpy as np
from sympy import (
    Expr,
    Rational,
    Symbol,
    cos,
    diff,
    expand,
    factorial,
    factorial2,
    sin,
    trigsimp,
)

from .legendre_polynomials import legendre

x = Symbol("x")
th = Symbol("θ")


class AssLegendreStore:
    def __init__(self):
        self.reset()

    def reset(self, definition=True, recursion=True):
        # Stores differentiation of the Legendre polynomials when using def
        if definition:
            self.definition: Dict[int, List[Expr]] = {}

        # Stores the Legendre functions when using rec
        if recursion:
            self.recursion: Dict[int, List[Expr]] = {}


ass_legendre_store = AssLegendreStore()


def associated_legendre_def(
    n: int,
    m: int,
    polar: bool = False,
    eval: int | float | np.ndarray | None = None,
    store: bool = True,
):
    if abs(m) > n:
        return x * 0 if eval is None else 0 * eval
    elif m < 0:
        m = -m
        if eval is None:
            return (
                (1 if m % 2 == 0 else -1)
                * factorial(n - m)
                / factorial(n + m)
                * associated_legendre_def(
                    n,
                    m,
                    polar=polar,
                    eval=eval,
                    store=store,
                )
            )
        else:
            return (
                (1 if m % 2 == 0 else -1)
                * fact(n - m)
                / fact(n + m)
                * associated_legendre_def(
                    n,
                    m,
                    polar=polar,
                    eval=eval,
                    store=store,
                )
            )
    elif m == 0:
        if eval is None:
            return legendre(n, polar=polar)
        else:
            return legendre(n, eval=eval, polar=polar)

    fun: Expr
    if store:
        if n not in ass_legendre_store.definition:
            ass_legendre_store.definition[n] = [legendre(n)]
        for i in range(len(ass_legendre_store.definition[n]), m + 1):
            ass_legendre_store.definition[n].append(
                expand(diff(ass_legendre_store.definition[n][i - 1], x, 1))
            )
        fun = expand((1 - x**2) ** Rational(m, 2) * ass_legendre_store.definition[n][m])
    else:
        fun = expand(
            (1 - x**2) ** Rational(m, 2)
            * diff(
                legendre(n),
                x,
                m,
            )
        )

    if eval is None:
        return (
            trigsimp(fun.subs((1 - x**2) ** Rational(1, 2), sin(th)).subs(x, cos(th)))
            if polar
            else fun
        )
    else:
        if isinstance(eval, (int, float)):
            if polar:
                eval = cosine(eval)
            return float(fun.subs(x, eval))
        else:
            if polar:
                eval = np.cos(eval)
            return np.vectorize(lambda val: float(fun.subs(x, val)))(eval)


def associated_legendre_rec(
    n: int,
    m: int,
    polar: bool = False,
    eval: int | float | np.ndarray | None = None,
    store: bool = True,
):
    if abs(m) > n:
        return x * 0 if eval is None else 0 * eval
    elif m < 0:
        m = -m
        if eval is None:
            return (
                (1 if m % 2 == 0 else -1)
                * factorial(n - m)
                / factorial(n + m)
                * associated_legendre_rec(
                    n,
                    m,
                    polar=polar,
                    eval=eval,
                    store=store,
                )
            )
        else:
            return (
                (1 if m % 2 == 0 else -1)
                * fact(n - m)
                / fact(n + m)
                * associated_legendre_rec(
                    n,
                    m,
                    polar=polar,
                    eval=eval,
                    store=store,
                )
            )
    elif m == 0 or m == 1:
        return associated_legendre_def(n, m, polar=polar, eval=eval, store=store)
    else:
        if store:
            if n not in ass_legendre_store.recursion:
                ass_legendre_store.recursion[n] = [
                    associated_legendre_rec(n, 0),
                    associated_legendre_rec(n, 1),
                ]
            for i in range(len(ass_legendre_store.recursion[n]), m + 1):
                ass_legendre_store.recursion[n].append(
                    expand(
                        (
                            2
                            * (i - 1)
                            * x
                            * (1 - x**2) ** Rational(-1, 2)
                            * ass_legendre_store.recursion[n][i - 1]
                            - (n + i - 1)
                            * (n - i + 2)
                            * ass_legendre_store.recursion[n][i - 2]
                        ),
                        deep=True,
                        mul=True,
                        multinomial=False,
                        power_exp=False,
                        power_base=False,
                        log=False,
                    ),
                )
            if eval is None:
                return (
                    trigsimp(
                        ass_legendre_store.recursion[n][m]
                        .subs((1 - x**2) ** Rational(1, 2), sin(th))
                        .subs(x, cos(th))
                    )
                    if polar
                    else ass_legendre_store.recursion[n][m]
                )
            else:
                if isinstance(eval, (int, float)):
                    if polar:
                        eval = cosine(eval)
                    return float(ass_legendre_store.recursion[n][m].subs(x, eval))
                else:
                    if polar:
                        eval = np.cos(eval)
                    return np.vectorize(
                        lambda val: float(ass_legendre_store.recursion[n][m].subs(x, val))
                    )(eval)
        else:
            if eval is not None and polar:
                eval = cosine(eval) if isinstance(eval, (int, float)) else np.cos(eval)
            prev_fun, curr_fun = (
                associated_legendre_rec(n, 0, polar=polar and eval is not None, eval=eval),
                associated_legendre_rec(n, 1, polar=polar and eval is not None, eval=eval),
            )
            for i in range(2, m + 1):
                prev_fun, curr_fun = (
                    curr_fun,
                    (
                        expand(
                            (
                                2 * (m - 1) * x * (1 - x**2) ** Rational(-1, 2) * curr_fun
                                - (n + m - 1) * (n - m + 2) * prev_fun
                            ),
                            deep=True,
                            mul=True,
                            multinomial=False,
                            power_exp=False,
                            power_base=False,
                            log=False,
                        )
                        if eval is None
                        else (
                            2
                            * (m - 1)
                            * eval
                            * (
                                sqrt(1 - eval**2)
                                if isinstance(eval, (int, float))
                                else np.sqrt(1 - eval**2)
                            )
                            * curr_fun
                            - (n + m - 1) * (n - m + 2) * prev_fun
                        )
                    ),
                )

            if polar and eval is None:
                curr_fun: Expr = trigsimp(
                    curr_fun.subs((1 - x**2) ** Rational(1, 2), sin(th)).subs(x, cos(th))
                )
            return curr_fun


def associated_legendre_rec_alt(
    n: int,
    m: int,
    polar: bool = False,
    eval: int | float | np.ndarray | None = None,
):
    if abs(m) > n:
        return x * 0 if eval is None else 0 * eval
    elif m == 0 or m == 1:
        return associated_legendre_def(n, m, polar=polar, eval=eval, store=False)
    elif m < 0:
        m = -m
        if eval is None:
            return (
                (1 if m % 2 == 0 else -1)
                * factorial(n - m)
                / factorial(n + m)
                * associated_legendre_rec_alt(
                    n,
                    m,
                    polar=polar,
                    eval=eval,
                )
            )
        else:
            return (
                (1 if m % 2 == 0 else -1)
                * fact(n - m)
                / fact(n + m)
                * associated_legendre_rec_alt(
                    n,
                    m,
                    polar=polar,
                    eval=eval,
                )
            )
    else:
        if eval is not None and polar:
            eval = cosine(eval) if isinstance(eval, (int, float)) else np.cos(eval)
        fun, pos_fun = None, None
        if eval is None:
            fun: Expr = expand(
                (factorial2(2 * m - 1) * (1 - x**2) ** Rational(m, 2)),
                deep=True,
                mul=True,
                multinomial=False,
                power_exp=False,
                power_base=False,
                log=False,
            )
            pos_fun: Expr = expand(
                ((2 * m + 1) * x * fun),
                deep=True,
                mul=True,
                multinomial=False,
                power_exp=False,
                power_base=False,
                log=False,
            )
        else:
            fun = float(factorial2(2 * m - 1)) * (
                pow(1 - eval**2, m / 2)
                if isinstance(eval, (int, float))
                else np.power(1 - eval**2, m / 2)
            )
            pos_fun = (2 * m + 1) * eval * fun
        for i in range(m + 1, n):
            fun, pos_fun = (
                pos_fun,
                (
                    expand(
                        ((2 * i + 1) * x * pos_fun - (i + m) * fun) / (i - m + 1),
                        deep=True,
                        mul=True,
                        multinomial=False,
                        power_exp=False,
                        power_base=False,
                        log=False,
                    )
                    if eval is None
                    else ((2 * i + 1) * eval * pos_fun - (i + m) * fun) / (i - m + 1)
                ),
            )
        if n == m:
            pos_fun = fun
        if polar and eval is None:
            pos_fun: Expr = trigsimp(
                pos_fun.subs((1 - x**2) ** Rational(1, 2), sin(th)).subs(x, cos(th))
            )
        return pos_fun


def associated_legendre(
    n: int,
    m: int,
    polar: bool = False,
    eval: int | float | np.ndarray | None = None,
) -> Expr | float | np.ndarray:
    """
    Calculate the analytical expression of the Associated Legendre function.

    Args:
        n (int): The subscript of the function.
            Must be an integer greater than or equal to 0.
        m (int): The superscript of the function.
            Must be an integer.
        polar (bool): If True, the function is returned in polar coordinates.
        eval (int, float, np.ndarray, None): The value(s) at which the function is evaluated.
            If None, the function is returned as an expression.
            Default is None.

    Returns:
        Expr | float | np.ndarray: The Associated Legendre function for the given subscript and superscript.

    Examples:
        ... code:: python

            >>> associated_legendre(1, 0)
            x
            >>> associated_legendre(1, 1, polar=True)
            sin(θ)
    """  # noqa: E501
    try:
        n = int(n)
        m = int(m)
    except ValueError:
        raise TypeError("n and m must both be integers")

    if eval is not None:
        if not isinstance(eval, (int, float)):
            try:
                eval = np.asarray(eval, dtype=float)
            except ValueError:
                raise TypeError("eval must be a number, an ndarray, or None")

    if m != 0 and (n / m < 8 or eval is not None):
        return associated_legendre_rec_alt(n, m, polar=polar, eval=eval)
    else:
        return associated_legendre_def(n, m, polar=polar, eval=eval)
