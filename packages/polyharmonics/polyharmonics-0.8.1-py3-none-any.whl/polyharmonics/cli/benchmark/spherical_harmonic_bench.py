import time
from multiprocessing import Process
from typing import List, Tuple

import pandas as pd
import typer
from rich.console import Console
from rich.status import Status
from tabulate import tabulate

from polyharmonics.cli.plotbench_cmd import plot_spherical_harmonic
from polyharmonics.spherical_harmonics import spherical_harmonic

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
console = Console()


def spherical_harmonic_bench_command(
    nm: str = typer.Argument(
        ...,
        help="""Calculate the spherical harmonics for the given subscripts and superscripts.
        Either a pair of integers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
        metavar="SUB:SUP",
    ),
    evaluate: str = typer.Option(
        None,
        "--eval",
        case_sensitive=False,
        help="""Evaluate the functions on the given numbers (θ, φ).
        Must be a pair of numbers separated by ':'.""",
    ),
    max_time: float = typer.Option(
        60.0,
        "--max-time",
        case_sensitive=False,
        help="Maximum execution time in seconds for each calculation. Default is 60 seconds.",  # noqa: E501
    ),
    csv: str = typer.Option(
        None,
        "--csv",
        case_sensitive=False,
        help="""Save the results in a CSV file with the given name.
        File extension must not be specified.""",
    ),
    plot: bool = typer.Option(
        False,
        "--plot",
        case_sensitive=False,
        help="Plot the results in a graph.",
    ),
) -> None:
    """Benchmark the calculation of spherical harmonics and display the time taken."""  # noqa: E501

    nm_values: List[Tuple[int, int]] = []
    try:
        for value in nm.split(","):
            n, m = value.split(":")
            if n is None or m is None or n == "" or m == "":
                raise typer.BadParameter(
                    "nm must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
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
            "nm must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
        )

    th: float
    phi: float
    if evaluate is not None:
        for value in evaluate.split(","):
            try:
                th, phi = value.split(":")
                th = float(th)
                phi = float(phi)
            except ValueError:
                raise typer.BadParameter("eval must be a pair of numbers separated by ':'.")

    with console.status(status="", spinner="dots") as status:
        status: Status
        headers = [
            "Yₙᵐ" + (" eval" if evaluate is not None else " calc"),
            "Definition",
        ]
        df = pd.DataFrame(columns=headers)
        n_tests = len(df.columns) - 1

        timed_out = [False for _ in range(n_tests)]
        for n, m in nm_values:
            # List of tests to run for each n, m of nm_values
            tests = [
                {
                    "fun": calculate_spherical_harmonic,
                    "args": (
                        n,
                        m,
                        None if evaluate is None else (th, phi),
                    ),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} "
                        f"Y{str(n).translate(SUB)}{str(m).translate(SUP)}({'θ, φ' if evaluate is None else (evaluate[0] + ', ' + evaluate[1])}) "  # noqa: E501
                        "with the definition."
                    ),
                },
            ]
            assert len(tests) == n_tests
            row = {"Yₙᵐ" + (" eval" if evaluate is not None else " calc"): f"{n}:{m}"}
            for n_test, test in enumerate(tests):
                status.update(f"[bold yellow1]{test['text']}[/]")
                if timed_out[n_test]:
                    row[headers[n_test + 1]] = "TIMEOUT"
                else:
                    legendre_calc = Process(target=test["fun"], args=test["args"])
                    t_start = time.time()
                    legendre_calc.start()
                    while legendre_calc.is_alive():
                        if time.time() - t_start > max_time:
                            legendre_calc.terminate()
                            row[headers[n_test + 1]] = "TIMEOUT"
                            timed_out[n_test] = True
                            break

                    if len(row) == n_test + 1:
                        row[headers[n_test + 1]] = round(time.time() - t_start, 6)

            df.loc[len(df)] = row

    if csv is None:
        console.print("[bold green]SPHERICAL HARMONICS   N:M[/]")
        console.print(
            tabulate(
                df,
                headers="keys",
                tablefmt="fancy_grid",
                maxheadercolwidths=[None] + [12 for _ in range(n_tests)],
                showindex=False,
            )
        )
    else:
        if not csv.endswith(".csv"):
            csv += ".csv"
        df.to_csv(csv, encoding="utf-8", index=False)

    if plot:
        plot_spherical_harmonic(df, evaluate is not None)

    raise typer.Exit()


def calculate_spherical_harmonic(
    n: int,
    m: int,
    evaluate: Tuple[float, float],
) -> None:
    spherical_harmonic(n, m, eval=evaluate)
