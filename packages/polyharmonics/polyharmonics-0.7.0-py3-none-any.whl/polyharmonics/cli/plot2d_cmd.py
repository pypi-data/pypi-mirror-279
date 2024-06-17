from math import pi
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import typer
from rich.console import Console

from polyharmonics import associated_legendre, legendre

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
    title: str = typer.Option(
        None,
        "--title",
        case_sensitive=False,
        help="Title of the plot.",
    ),
    x_lim: str = typer.Option(
        None,
        "--xlim",
        case_sensitive=False,
        help="Limits for the x-axis as two numbers separated by a comma.",
    ),
    y_lim: str = typer.Option(
        None,
        "--ylim",
        case_sensitive=False,
        help="Limits for the y-axis as two numbers separated by a comma.",
    ),
    equal_axes: bool = typer.Option(
        False,
        "--eq-axes",
        case_sensitive=False,
        help="Set equal scaling (proportion 1:1) on both axes.",
    ),
    center_axes: bool = typer.Option(
        False,
        "--center-axes",
        case_sensitive=False,
        help="Fix axes at the center of the plot, passing through (0, 0).",
    ),
    show_grid: bool = typer.Option(
        False, "--grid", case_sensitive=False, help="Show grid lines."
    ),
    polar: bool = typer.Option(
        False, "--polar", case_sensitive=False, help="Plot in polar coordinates."
    ),
) -> None:
    """Plot the 2D functions given by this package."""

    n_values: List[int] = []
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
    except AttributeError:
        pass

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
    except AttributeError:
        pass

    if not n_values and not nm_values:
        raise typer.BadParameter("No functions to plot.")

    if x_lim is not None:
        try:
            x_lim = [float(value) for value in x_lim.split(",")]
            if len(x_lim) != 2:
                raise ValueError
        except ValueError:
            raise typer.BadParameter("x_lim must be two numbers separated by a comma.")
    if y_lim is not None:
        try:
            y_lim = [float(value) for value in y_lim.split(",")]
            if len(y_lim) != 2:
                raise ValueError
        except ValueError:
            raise typer.BadParameter("y_lim must be two numbers separated by a comma.")

    x = np.linspace(0 if polar else -1, pi if polar else 1, 500)

    plt.figure(figsize=(10, 6))

    for n in n_values:
        y = [legendre(n, eval=xi, polar=polar) for xi in x]
        plt.plot(x, y, label=f"$P_{n}(x)$")

    for n, m in nm_values:
        y = [associated_legendre(n, m, eval=xi, polar=polar) for xi in x]
        plt.plot(x, y, label=f"$P_{n}^{m}(x)$")

    if title:
        plt.title(title)
    if x_lim:
        plt.xlim(x_lim)
    if y_lim:
        plt.ylim(y_lim)
    if equal_axes:
        plt.gca().set_aspect("equal", adjustable="box")
    if center_axes:
        ax = plt.gca()
        ax.spines["left"].set_position("zero")
        ax.spines["left"].set_color("black")
        ax.spines["left"].set_linewidth(0.5)
        ax.spines["bottom"].set_position("zero")
        ax.spines["bottom"].set_color("black")
        ax.spines["bottom"].set_linewidth(0.5)
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_tick_params(direction="in", which="both")
        ax.yaxis.set_tick_params(direction="in", which="both")

    plt.legend()
    plt.grid(show_grid)
    plt.show()

    raise typer.Exit()
