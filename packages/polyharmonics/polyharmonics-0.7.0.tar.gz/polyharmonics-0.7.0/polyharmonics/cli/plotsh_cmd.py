from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import typer
from rich.console import Console

from polyharmonics import spherical_harmonic

console = Console()


def plotsh_command(
    nm: str = typer.Argument(
        ...,
        help="""The corresponding subscript(s) and superscript(s) of the function(s).
        Either a pair of integers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
        metavar="SUB:SUP",
    ),
) -> None:
    """Plot the spherical harmonics given by this package."""

    try:
        n_values: List[int] = []
        m_values: List[int] = []
        for value in nm.split(","):
            n, m = value.split(":")
            if n is None or m is None or n == "" or m == "":
                raise typer.BadParameter(
                    "nm must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
                )
            else:
                n_values.append(int(n))
                m_values.append(int(m))
        if any(i < 0 for i in n_values):
            raise typer.BadParameter("All subscripts must be greater or equal to 0.")
    except ValueError:
        raise typer.BadParameter(
            "nm must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
        )

    raise typer.Exit()
