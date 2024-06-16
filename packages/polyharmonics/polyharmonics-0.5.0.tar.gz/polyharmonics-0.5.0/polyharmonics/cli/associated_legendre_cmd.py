from time import time
from typing import List, Optional

import typer
from rich.console import Console
from sympy import Expr, latex, pretty

from polyharmonics import associated_legendre

from .colors import Color

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
console = Console()


def associated_legendre_command(
    nm: str = typer.Argument(
        ...,
        help="""The corresponding subscript(s) and superscript(s) of the function(s).
        Either a pair of integers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
        metavar="SUB:SUP",
    ),
    print_latex: bool = typer.Option(
        False,
        "-l",
        "--latex",
        case_sensitive=False,
        help="Print the function(s) in LaTeX format.",
    ),
    polar: bool = typer.Option(
        False,
        "-p",
        "--polar",
        case_sensitive=False,
        help="Calculate the function(s) with polar coordinates.",
    ),
    evaluate: str = typer.Option(
        None,
        "--eval",
        case_sensitive=False,
        help="""Print the function(s) evaluated on the given numbers.
        Either a number or a comma-separated list of numbers.""",
    ),
    color: Optional[Color] = typer.Option(
        Color.white,
        "-c",
        "--color",
        case_sensitive=False,
        help="Color for print. White if not specified.",
    ),
    display_time: bool = typer.Option(
        False,
        "-t",
        "--time",
        case_sensitive=False,
        help="Display the time taken to calculate the function(s).",
    ),
) -> None:
    """Calculate and print the associated Legendre function(s)."""

    if print_latex and evaluate:
        raise typer.BadParameter(
            "Cannot use both '--print_latex' and '--eval' at the same time."
        )

    # Convert the input to two lists of integers
    try:
        n_values: List[int] = []
        m_values: List[int] = []
        for value in nm.split(","):
            n, m = value.split(":")
            if n is None or m is None or n == "" or m == "":
                raise typer.BadParameter(
                    "Between each ',' must be a pair of integers separated by ':'."
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

    x_values: List[float] = []
    if evaluate is not None:
        for value in evaluate.split(","):
            try:
                x_values.append(float(value))
            except ValueError:
                raise typer.BadParameter(
                    "eval must either be a number or a list of numbers separated by commas."
                )

    if display_time:
        t_start = time()

    # Calculate the Associated Legendre function(s)

    with console.status(
        status=(
            "[yellow1]Calculating associated Legendre functions.[/]"
            if len(n_values) > 1
            else "[yellow1]Calculating associated Legendre function.[/]"
        ),
        spinner="dots",
    ):
        if x_values:
            result: List[List[float]] = [
                [associated_legendre(i, j, polar=polar, eval=x) for x in x_values]
                for i, j in zip(n_values, m_values)
            ]
        else:
            result: List[Expr] = [
                associated_legendre(i, j, polar=polar) for i, j in zip(n_values, m_values)
            ]

    if display_time:
        t_end = time()
        console.print(
            f"[bold green1]Done! [/][bold]Time taken: {t_end - t_start:.6f} seconds[/]\n"  # noqa: E501
        )

    for n, m, fun in zip(n_values, m_values, result):
        if print_latex:
            if polar:
                console.print(
                    f"[bold {color}]P_{n}^{m}(\\cos(\\theta)) = {latex(fun)}[/]\n"
                )
            else:
                console.print(f"[bold {color}]P_{n}^{m}(x) = {latex(fun)}[/]\n")
        elif x_values:
            for i, x in enumerate(x_values):
                if polar:
                    console.print(
                        f"[bold {color}]P{str(n).translate(SUB)}{str(m).translate(SUP)}(cos({x})) = {fun[i]}[/]\n"  # noqa: E501
                    )
                else:
                    console.print(
                        f"[bold {color}]P{str(n).translate(SUB)}{str(m).translate(SUP)}({x}) = {fun[i]}[/]\n"  # noqa: E501
                    )
        else:
            if polar:
                console.print(
                    f"[bold {color}]P{str(n).translate(SUB)}{str(m).translate(SUP)}(cos(θ)) = [/]"  # noqa: E501
                )
            else:
                console.print(
                    f"[bold {color}]P{str(n).translate(SUB)}{str(m).translate(SUP)}(x) = [/]"  # noqa: E501
                )
            console.print(
                f"[bold {color}] {pretty(fun)}[/]\n",
            )

    raise typer.Exit()
