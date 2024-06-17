from typing import List, Tuple

import typer
from rich.console import Console
from sympy import Expr, latex, pretty

from polyharmonics import legendre

from .colors import Color

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
console = Console()


def plot3d_command(
    plt_spherical_harmonic: str = typer.Option(
        None,
        "--spherical-harmonic",
        "--sh",
        case_sensitive=False,
        help="""Plot the spherical harmonic(s) of the given subscript(s) and superscript(s).
        Either a pair of integers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
        metavar="SUB:SUP",
    ),
) -> None:
    """Plot the 3D functions given by this package."""

    nm_values: List[Tuple[int, int]] = []
    try:
        for value in plt_spherical_harmonic.split(","):
            n, m = value.split(":")
            if n is None or m is None or n == "" or m == "":
                raise typer.BadParameter(
                    "spherical-harmonic must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
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
            "spherical-harmonic must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
        )

    if not nm_values:
        raise typer.BadParameter("No functions to plot.")

    raise typer.Exit()
