import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typer
from rich.console import Console
from scipy.interpolate import make_interp_spline

from .colors import Color

console = Console()


def plotbench_command(
    csv: str = typer.Argument(
        ...,
        help="""Path of the CSV file with the benchmark results.
        File extension must not be specified.""",
        metavar="PATH",
    ),
) -> None:
    """Plot the benchmark results from this package."""
    if not csv.endswith(".csv"):
        csv += ".csv"
    try:
        with open(csv, "r") as f:
            df = pd.read_csv(f)
            if len(df.columns) < 2:
                console.print(f"[bold {Color.red1}]Not enough columns in the CSV file.[/]")
                raise typer.Exit()
            if len(df) < 2:
                console.print(f"[bold {Color.red1}]Not enough rows in the CSV file.[/]")
                raise typer.Exit()
            fun_type = df.columns[0]
            evaluate = "eval" in fun_type
            for fun in FUN_TYPES:
                if fun in fun_type:
                    FUN_TYPES[fun](df=df, evaluate=evaluate)
                    raise typer.Exit()
            console.print(
                f"[bold {Color.red1}]CSV data doesn't correspond to any function type.[/]"
            )
            raise typer.Exit()

    except FileNotFoundError:
        console.print(f"[bold {Color.red1}]File not found: {csv}[/]")
        raise typer.Exit()


def plot_legendre(df: pd.DataFrame, evaluate: bool):
    df["Pₙ" + (" eval" if evaluate else " calc")] = df[
        "Pₙ" + (" eval" if evaluate else " calc")
    ].astype(int)
    columns = df.columns[1:]
    plt.figure(figsize=(10, 6))

    something_to_plot = False
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        clean_df = df.dropna(subset=[col])
        if clean_df[col].count() > 1:
            something_to_plot = True
            scatter = plt.scatter(
                clean_df["Pₙ" + (" eval" if evaluate else " calc")],
                clean_df[col],
                label=col,
            )
            x = clean_df["Pₙ" + (" eval" if evaluate else " calc")].values
            y = clean_df[col].values
            try:
                spline = make_interp_spline(x, y, k=3)
                X_ = np.linspace(x.min(), x.max(), 500)
                Y_ = spline(X_)

                plt.plot(X_, Y_, linestyle="--", color=scatter.get_facecolor()[0])
            except ValueError as e:
                print(f"Could not fit spline for {col}: {e}")

    if not something_to_plot:
        console.print(f"[bold {Color.red1}]Not enough data to plot.[/]")
        return
    plt.xlabel("First N polynomials")
    plt.ylabel("Time (s)")
    plt.title(
        f"{'Evaluation' if evaluate else 'Calculation'} of Legendre polynomials $P_n(x)$"
    )
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_associated_legendre(df: pd.DataFrame, evaluate: bool):
    df[["N", "M"]] = df["Pₙᵐ" + (" eval" if evaluate else " calc")].str.split(
        ":", expand=True
    )
    df["N"] = df["N"].astype(int)
    df["M"] = df["M"].astype(int)

    columns = df.columns[1:-2]
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    max_limit = max(df["N"].max(), df["M"].max()) + 10

    for i, label in enumerate(columns):
        plt.figure(num=i + 1, figsize=(10, 6))
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


def plot_spherical_harmonic(df: pd.DataFrame, evaluate: bool):
    df[["N", "M"]] = df["Yₙᵐ" + (" eval" if evaluate else " calc")].str.split(
        ":", expand=True
    )
    df["N"] = df["N"].astype(int)
    df["M"] = df["M"].astype(int)

    columns = df.columns[1:-2]
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    max_limit = max(df["N"].max(), df["M"].max()) + 10

    for i, label in enumerate(columns):
        plt.figure(num=i + 1, figsize=(10, 6))
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


FUN_TYPES = {
    "Pₙ ": plot_legendre,
    "Pₙᵐ ": plot_associated_legendre,
    "Yₙᵐ ": plot_spherical_harmonic,
}
