from time import time
from typing import List, Optional

import typer
from rich.console import Console
from sympy import Expr, latex, pretty

from polyharmonics import legendre

from .colors import Color

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
console = Console()


def legendre_command(
    n: str = typer.Argument(
        ...,
        help="""The degree of the polynomial(s).
        An integer or a comma-separated list of integers.""",
        metavar="DEGREE",
    ),
    print_latex: bool = typer.Option(
        False,
        "-l",
        "--latex",
        case_sensitive=False,
        help="Print the polynomial(s) in LaTeX format.",
    ),
    evaluate: str = typer.Option(
        None,
        "--eval",
        case_sensitive=False,
        help="""Print the polynomial(s) evaluated on the given numbers.
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
    """Calculate and print the Legendre polynomial(s)."""

    if print_latex and evaluate:
        raise typer.BadParameter(
            "Cannot use both '--print_latex' and '--eval' at the same time."
        )

    # Convert the input to a list of integers
    try:
        n_values: List[int] = [int(value) for value in n.split(",")]
        if any(i < 0 for i in n_values):
            raise typer.BadParameter("All integers must be greater or equal to 0.")
    except ValueError:
        raise typer.BadParameter(
            "n must be an integer or a comma-separated list of integers."
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

    # Calculate the Legendre polynomial(s)

    with console.status(
        status=(
            "[yellow1]Calculating Legendre polynomials.[/]"
            if len(n_values) > 1
            else "[yellow1]Calculating Legendre polynomial.[/]"
        ),
        spinner="dots",
    ):
        if x_values:
            result: List[List[float]] = [
                [legendre(i, x) for x in x_values] for i in n_values
            ]
        else:
            result: List[Expr] = [legendre(i) for i in n_values]

    if display_time:
        t_end = time()
        console.print(
            f"[bold green1]Done! [/][bold]Time taken: {t_end - t_start:.6f} seconds[/]\n"  # noqa: E501
        )

    for n, pol in zip(n_values, result):
        if print_latex:
            console.print(f"[bold {color}]P_{n}(x) = {latex(pol)}[/]\n")
        elif x_values:
            for i, x in enumerate(x_values):
                console.print(
                    f"[bold {color}]P{str(n).translate(SUB)}({x}) = {pol[i]}[/]\n"
                )
        else:
            console.print(f"[bold {color}]P{str(n).translate(SUB)}(x) = [/]")
            console.print(f"[bold {color}] {pretty(pol)}[/]\n")

    raise typer.Exit()
