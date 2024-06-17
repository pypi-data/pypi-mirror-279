from time import time
from typing import List, Optional

import typer
from rich.console import Console
from sympy import Expr, latex, pretty

from polyharmonics import spherical_harmonic

from .colors import Color

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
console = Console()


def spherical_harmonic_command(
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
    evaluate: str = typer.Option(
        None,
        "--eval",
        case_sensitive=False,
        help="""Print the function(s) evaluated on the given numbers (θ, φ).
        Either a pair of numbers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
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
    """Calculate and print the spherical harmonic(s)."""

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

    th_values: List[float] = []
    phi_values: List[float] = []
    if evaluate is not None:
        for value in evaluate.split(","):
            try:
                th, phi = value.split(":")
                th_values.append(float(th))
                phi_values.append(float(phi))
            except ValueError:
                raise typer.BadParameter(
                    "eval must either be a pair of numbers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
                )

    if display_time:
        t_start = time()

    # Calculate the spherical harmoinc(s)

    with console.status(
        status=(
            "[yellow1]Calculating spherical harmonics.[/]"
            if len(n_values) > 1
            else "[yellow1]Calculating spherical harmonic.[/]"
        ),
        spinner="dots",
    ):
        if th_values and phi_values:
            result: List[List[float]] = [
                [
                    spherical_harmonic(i, j, eval=(th, phi))
                    for th, phi in zip(th_values, phi_values)
                ]
                for i, j in zip(n_values, m_values)
            ]
        else:
            result: List[Expr] = [
                spherical_harmonic(i, j) for i, j in zip(n_values, m_values)
            ]

    if display_time:
        t_end = time()
        console.print(
            f"[bold green1]Done! [/][bold]Time taken: {t_end - t_start:.6f} seconds[/]\n"  # noqa: E501
        )

    for n, m, fun in zip(n_values, m_values, result):
        if print_latex:
            console.print(f"[bold {color}]Y_{n}^{m}(\\theta, \\varphi) = {latex(fun)}[/]\n")
        elif th_values and phi_values:
            for i, (th, phi) in enumerate(zip(th_values, phi_values)):
                console.print(
                    f"[bold {color}]Y{str(n).translate(SUB)}{str(m).translate(SUP)}({th}, {phi}) = {fun[i]}[/]\n"  # noqa: E501
                )
        else:
            console.print(
                f"[bold {color}]P{str(n).translate(SUB)}{str(m).translate(SUP)}(θ, φ) = [/]"  # noqa: E501
            )
            console.print(
                f"[bold {color}] {pretty(fun)}[/]\n",
            )

    raise typer.Exit()
