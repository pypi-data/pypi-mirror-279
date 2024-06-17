from typing import List, Tuple

import typer
from rich.console import Console
from sympy import Expr, latex, pretty

from polyharmonics import legendre

from .colors import Color

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
console = Console()


def plot2d_command(
    plt_legendre: str = typer.Option(
        None,
        "--legendre",
        "--l",
        case_sensitive=False,
        help="""Plot the Legendre polynomial(s) of the given degree(s).
        Either a number or a comma-separated list of numbers.""",
        metavar="DEGREE",
    ),
    plt_associated_legendre: str = typer.Option(
        None,
        "--associated-legendre",
        "--al",
        case_sensitive=False,
        help="""Plot the associated Legendre function(s) of the given subscript(s) and superscript(s).
        Either a pair of integers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
        metavar="SUB:SUP",
    ),
) -> None:
    """Plot the 2D functions given by this package."""

    try:
        n_values = sorted([int(value) for value in plt_legendre.split(",")])
        if any(i < 0 for i in n_values):
            raise typer.BadParameter(
                "All integers must be greater or equal to 0."  # noqa: E501
            )
    except ValueError:
        raise typer.BadParameter(
            "legendre must be an integer or a comma-separated list of integers."  # noqa: E501
        )

    nm_values: List[Tuple[int, int]] = []
    try:
        for value in plt_associated_legendre.split(","):
            n, m = value.split(":")
            if n is None or m is None or n == "" or m == "":
                raise typer.BadParameter(
                    "associated-legendre must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
                )
            else:
                nm_values.append((int(n), int(m)))

        nm_values.sort(key=lambda x: (x[0], x[1]))
        if any(n < 0 for n, m in nm_values):
            raise typer.BadParameter(
                "All subscripts must be greater or equal to 0."  # noqa: E501
            )
    except ValueError:
        raise typer.BadParameter(
            "associated-legendre must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
        )

    if not n_values and not nm_values:
        raise typer.BadParameter("No functions to plot.")

    raise typer.Exit()
