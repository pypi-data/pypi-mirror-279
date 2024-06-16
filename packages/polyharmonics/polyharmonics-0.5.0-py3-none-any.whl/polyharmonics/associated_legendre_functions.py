from typing import Dict, List

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
    eval: float | None = None,
    store: bool = True,
):
    if abs(m) > n:
        return x * 0
    elif m < 0:
        return (
            (1 if m % 2 == 0 else -1)
            * factorial(n - m)
            / factorial(n + m)
            * associated_legendre_def(
                n,
                -m,
                polar=polar,
                eval=eval,
                store=store,
            )
        )
    elif m == 0:
        if eval is None:
            return legendre(n).subs(x, cos(th)) if polar else legendre(n)
        else:
            return legendre(n, eval=cos(eval)) if polar else legendre(n, eval=eval)

    fun: Expr = None
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

    if polar:
        return (
            trigsimp(fun.subs((1 - x**2) ** Rational(1, 2), sin(th)).subs(x, cos(th)))
            if eval is None
            else fun.subs((1 - x**2) ** Rational(1, 2), sin(th))
            .subs(x, cos(th))
            .subs(th, eval)
        )
    else:
        return fun if eval is None else fun.subs(x, eval)


def associated_legendre_rec(
    n: int,
    m: int,
    polar: bool = False,
    eval: bool | None = None,
    store: bool = True,
):
    if abs(m) > n:
        return x * 0
    elif m < 0:
        return (
            (1 if m % 2 == 0 else -1)
            * factorial(n - m)
            / factorial(n + m)
            * associated_legendre_rec(n, -m, polar=polar, eval=eval, store=store)
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
            if polar:
                return (
                    trigsimp(
                        ass_legendre_store.recursion[n][m]
                        .subs((1 - x**2) ** Rational(1, 2), sin(th))
                        .subs(x, cos(th))
                    )
                    if eval is None
                    else ass_legendre_store.recursion[n][m]
                    .subs((1 - x**2) ** Rational(1, 2), sin(th))
                    .subs(x, cos(th))
                    .subs(th, eval)
                )
            else:
                return (
                    ass_legendre_store.recursion[n][m]
                    if eval is None
                    else ass_legendre_store.recursion[n][m].subs(x, eval)
                )
        else:
            if eval is not None and polar:
                eval = cos(eval)
            prev_fun: Expr = (
                associated_legendre_rec(n, 0)
                if eval is None
                else associated_legendre_rec(n, 0, polar=polar, eval=eval)
            )
            curr_fun: Expr = (
                associated_legendre_rec(n, 1)
                if eval is None
                else associated_legendre_rec(n, 1, polar=polar, eval=eval)
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
                            2 * (m - 1) * eval * (1 - eval**2) ** Rational(-1, 2) * curr_fun
                            - (n + m - 1) * (n - m + 2) * prev_fun
                        )
                    ),
                )

            if polar and eval is None:
                curr_fun = trigsimp(
                    curr_fun.subs((1 - x**2) ** Rational(1, 2), sin(th)).subs(x, cos(th))
                )
            return curr_fun


def associated_legendre_rec_alt(
    n: int,
    m: int,
    polar: bool = False,
    eval: float | None = None,
):
    if abs(m) > n:
        return x * 0
    elif m == 0 or m == 1:
        return associated_legendre_def(n, m, polar=polar, eval=eval, store=eval is None)
    elif m < 0:
        return (
            (1 if m % 2 == 0 else -1)
            * factorial(n - m)
            / factorial(n + m)
            * associated_legendre_rec_alt(n, -m, polar=polar, eval=eval)
        )
    else:
        if eval is not None and polar:
            eval = cos(eval)
        fun: Expr = expand(
            (
                factorial2(2 * m - 1) * (1 - x**2) ** Rational(m, 2)
                if eval is None
                else factorial2(2 * m - 1) * (1 - eval**2) ** Rational(m, 2)
            ),
            deep=True,
            mul=True,
            multinomial=False,
            power_exp=False,
            power_base=False,
            log=False,
        )
        pos_fun: Expr = expand(
            ((2 * m + 1) * x * fun if eval is None else (2 * m + 1) * eval * fun),
            deep=True,
            mul=True,
            multinomial=False,
            power_exp=False,
            power_base=False,
            log=False,
        )
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
        if m == n:
            pos_fun = fun
        if polar and eval is None:
            pos_fun = trigsimp(
                pos_fun.subs((1 - x**2) ** Rational(1, 2), sin(th)).subs(x, cos(th))
            )
        return pos_fun


def associated_legendre(
    n: int,
    m: int,
    polar: bool = False,
    eval: float | None = None,
) -> Expr:
    """
    Calculate the analytical expression of the Associated legendre function

    Args:
        n (int): The subscript of the function.
            Must be an integer greater than or equal to 0.
        m (int): The superscript of the function.
            Must be an integer.
        polar (bool): If True, the function is returned in polar coordinates.
        eval (int, float, None): The value at which the function is evaluated.
            If None, the function is returned as an expression.
            Default is None.

    Returns:
        Expr: The Associated legendre function for the given subscript and superscript.

    Examples:
        ... code:: python

            >>> associated_legendre(1, 0)
            x
            >>> associated_legendre(1, 1, polar=True)
            sin(θ)
    """  # noqa: E501
    if not isinstance(n, int) or not isinstance(m, int):
        raise TypeError("n and m must both be integers")
    if n < 0:
        raise ValueError("n must be greater than or equal to 0")
    if isinstance(eval, int):
        eval = float(eval)
    if eval is not None and not isinstance(eval, float):
        raise TypeError("eval must be a number or None")
    if m != 0 and eval is not None:
        if eval == 1 or eval == -1:
            return 0
    return (
        associated_legendre_rec_alt(n, m, polar=polar, eval=eval)
        if m != 0 and (n / m < 8 or eval is not None)
        else associated_legendre_def(n, m, polar=polar)
    )
