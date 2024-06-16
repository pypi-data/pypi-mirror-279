import time
from multiprocessing import Process

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typer
from rich.console import Console
from rich.status import Status
from tabulate import tabulate

from polyharmonics.legendre_polynomials import (
    legendre_def,
    legendre_exp,
    legendre_rec,
    legendre_store,
)

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
console = Console()


def legendre_bench_command(
    n: str = typer.Argument(
        ...,
        help="""Calculate the Legendre polynomials from 0 to the given degree.
        An integer or a comma-separated list of integers.""",
        metavar="DEGREE",
    ),
    evaluate: float = typer.Option(
        None,
        "--eval",
        case_sensitive=False,
        help="Evaluate the polynomials on the given number.",
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
    """Benchmark the calculation of Legendre polynomials and display the time taken."""  # noqa: E501

    # Convert the Legendre input to a list of integers
    try:
        n_values = sorted([int(value) for value in n.split(",")])
        if any(i < 0 for i in n_values):
            raise typer.BadParameter(
                "All integers must be greater or equal to 0."  # noqa: E501
            )
    except ValueError:
        raise typer.BadParameter(
            "n must be an integer or a comma-separated list of integers."  # noqa: E501
        )

    with console.status(status="", spinner="dots") as status:
        status: Status
        headers = [
            "N",
            "Definition w storage",
            "Definition w/o storage",
            "Recursion w storage",
            "Recursion w/o storage",
            "Expression",
        ]
        df = pd.DataFrame(columns=headers)
        n_tests = len(df.columns) - 1

        # List for each test to indicate if it timed out
        timed_out = [False for _ in range(n_tests)]
        for i in n_values:
            # List of tests to run for each n of n_values
            tests = [
                {
                    "fun": calculate_legendre,
                    "args": (i, evaluate, True, True),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} all Legendre polynomials "  # noqa: E501
                        f"from P{str(0).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        f"to P{str(i).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        "with definition and storage."
                    ),
                },
                {
                    "fun": calculate_legendre,
                    "args": (i, evaluate, True, False),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} all Legendre polynomials "  # noqa: E501
                        f"from P{str(0).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        f"to P{str(i).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        "with definition but no storage."
                    ),
                },
                {
                    "fun": calculate_legendre,
                    "args": (i, evaluate, False, True),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} all Legendre polynomials "  # noqa: E501
                        f"from P{str(0).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        f"to P{str(i).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        "with recursion and storage."
                    ),
                },
                {
                    "fun": calculate_legendre,
                    "args": (i, evaluate, False, False),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} all Legendre polynomials "  # noqa: E501
                        f"from P{str(0).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        f"to P{str(i).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        "with recursion but no storage."
                    ),
                },
                {
                    "fun": calculate_legendre_exp,
                    "args": (i, evaluate),
                    "text": (
                        f"{'Calculating' if evaluate is None else 'Evaluating'} all Legendre polynomials "  # noqa: E501
                        f"from P{str(0).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        f"to P{str(i).translate(SUB)}({'x' if evaluate is None else evaluate}) "  # noqa: E501
                        "with the expression."
                    ),
                },
            ]
            assert len(tests) == n_tests
            row = {"N": i}
            for n_test, test in enumerate(tests):
                status.update(f"[yellow1]{test['text']}[/]")
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
        console.print(
            "[bold green]LEGENDRE POLYNOMIALS UP TO N[/]"
            + f"[bold green] EVALUATED ON x = {evaluate}[/]"
            if evaluate is not None
            else ""
        )
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


def calculate_legendre(n: int, evaluate: float | None, use_legendre_def: bool, store: bool):
    if store:
        # Reset the store to avoid following calculations to be faster than expected
        legendre_store.reset(definition=use_legendre_def, recursion=not use_legendre_def)
    for i in range(n + 1):
        if use_legendre_def:
            legendre_def(i, eval=evaluate, store=store)
        else:
            legendre_rec(i, eval=evaluate, store=store)


def calculate_legendre_exp(n: int, evaluate: float | None):
    for i in range(n + 1):
        legendre_exp(i, eval=evaluate)


def plot_results(df: pd.DataFrame, evaluate: bool):
    df["N"] = df["N"].astype(int)
    columns = df.columns[1:]
    console.print(columns)
    plt.figure(figsize=(10, 6))

    something_to_plot = False
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        clean_df = df.dropna(subset=[col])
        if clean_df[col].count() > 2:
            something_to_plot = True
            scatter = plt.scatter(clean_df["N"], clean_df[col], label=col)
            x = clean_df["N"]
            y = clean_df[col]
            try:
                X_ = np.linspace(x.min(), x.max(), 500)
                coeff = np.polyfit(x, y, 3)
                Y_ = np.polyval(coeff, X_)

                # Ensure the curve is monotonically increasing
                Y_ = np.maximum.accumulate(Y_)

                plt.plot(X_, Y_, linestyle="--", color=scatter.get_facecolor()[0])
            except ValueError as e:
                print(f"Could not fit curve for {col}: {e}")

    if not something_to_plot:
        raise ValueError("Not enough data to plot.")
    plt.xlabel("First N polynomials")
    plt.ylabel("Time (s)")
    plt.title(
        f"{'Evaluation' if evaluate else 'Calculation'} of Legendre polynomials $P_n(x)$"
    )
    plt.legend()
    plt.grid(True)
    plt.show()
