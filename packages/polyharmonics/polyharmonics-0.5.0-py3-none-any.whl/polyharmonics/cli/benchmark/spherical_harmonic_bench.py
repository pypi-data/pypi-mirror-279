import time
from multiprocessing import Process
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import typer
from rich.console import Console
from rich.status import Status
from tabulate import tabulate

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
                    "Between each ',' must be a pair of integers separated by ':'."  # noqa: E501
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
            "N:M",
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
                        f"Y{str(n).translate(SUB)}{str(m).translate(SUP)}{'x' if evaluate is None else evaluate} "  # noqa: E501
                        "with the definition."
                    ),
                },
            ]
            assert len(tests) == n_tests
            row = {"N:M": f"{n}:{m}"}
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
        df.to_csv(csv + ".csv", encoding="utf-8", index=False)

    if plot:
        plot_results(df, evaluate is not None)

    raise typer.Exit()


def calculate_spherical_harmonic(
    n: int,
    m: int,
    evaluate: Tuple[float, float],
) -> None:
    spherical_harmonic(n, m, eval=evaluate)


def plot_results(df: pd.DataFrame, evaluate: bool):
    df[["N", "M"]] = df["N:M"].str.split(":", expand=True)
    df["N"] = df["N"].astype(int)
    df["M"] = df["M"].astype(int)

    columns = df.columns[1:-2]
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    max_limit = max(df["N"].max(), df["M"].max()) + 10

    for i, label in enumerate(columns):
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(
            df["N"],
            df["M"],
            c=df[label],
            cmap="RdYlGn_r",
            s=100,
            alpha=0.7,
        )
        cbar = plt.colorbar(scatter)
        cbar.set_label("Time (s)")

        plt.xlabel("N")
        plt.ylabel("M")
        plt.title(
            f"{'Evaluation' if evaluate else 'Calculation'} of spherical harmonics $Y_n^m(θ, φ)$ - {label}"  # noqa: E501
        )
        plt.grid(True)

        plt.xlim(0, max_limit)
        plt.ylim(0, max_limit)

        plt.show()
