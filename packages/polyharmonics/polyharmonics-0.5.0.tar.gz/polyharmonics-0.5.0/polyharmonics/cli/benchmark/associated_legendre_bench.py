import time
from multiprocessing import Process
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import typer
from rich.console import Console
from rich.status import Status
from tabulate import tabulate

from polyharmonics.associated_legendre_functions import (
    ass_legendre_store,
    associated_legendre_def,
    associated_legendre_rec,
    associated_legendre_rec_alt,
)

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
console = Console()


def associated_legendre_bench_command(
    nm: str = typer.Argument(
        ...,
        help="""Calculate the associated Legendre functions for the given subscripts and superscripts.
        Either a pair of integers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
        metavar="SUB:SUP",
    ),
    evaluate: float = typer.Option(
        None,
        "--eval",
        case_sensitive=False,
        help="Evaluate the functions on the given number.",
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
    """Benchmark the calculation of associated Legendre functions and display the time taken."""  # noqa: E501

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

    with console.status(status="", spinner="dots") as status:
        status: Status
        headers = [
            "N:M",
            "Definition w storage",
            "Definition w/o storage",
            "Recursion w storage",
            "Recursion w/o storage",
            "Alternative recursion",
        ]
        df = pd.DataFrame(columns=headers)
        n_tests = len(df.columns) - 1

        timed_out = [False for _ in range(n_tests)]
        for n, m in nm_values:
            # List of tests to run for each n, m of nm_values
            tests = [
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, evaluate, True, False, True),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}{'x' if evaluate is None else evaluate} "  # noqa: E501
                        "with the definition and storage."
                    ),
                },
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, evaluate, True, False, False),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}{'x' if evaluate is None else evaluate} "  # noqa: E501
                        "with the definition but no storage."
                    ),
                },
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, evaluate, False, False, True),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}{'x' if evaluate is None else evaluate} "  # noqa: E501
                        "with the recursion and storage."
                    ),
                },
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, evaluate, False, False, False),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}{'x' if evaluate is None else evaluate} "  # noqa: E501
                        "with the recursion but no storage."
                    ),
                },
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, evaluate, False, True, False),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}{'x' if evaluate is None else evaluate} "  # noqa: E501
                        "with the alternative recursion."
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
        console.print("[bold green]ASSOCIATED LEGENDRE FUNCTIONS N:M[/]")
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


def calculate_associated_legendre(
    n: int,
    m: int,
    evaluate: float | None,
    use_def: bool,
    use_alt_rec: bool,
    store: bool,
):
    if store:
        # Reset the stores to avoid following calculations to be faster than expected
        ass_legendre_store.reset(
            definition=use_def,
            recursion=not use_def,
        )
    if use_alt_rec:
        associated_legendre_rec_alt(n, m, eval=evaluate)
    else:
        if use_def:
            associated_legendre_def(n, m, eval=evaluate, store=store)
        else:
            associated_legendre_rec(n, m, eval=evaluate, store=store)


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
            f"{'Evaluation' if evaluate else 'Calculation'} of associated Legendre functions $P_n^m(x)$ - {label}"  # noqa: E501
        )
        plt.grid(True)

        plt.xlim(0, max_limit)
        plt.ylim(0, max_limit)

        plt.show()
