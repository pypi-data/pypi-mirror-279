# type: ignore[attr-defined]
from typing import Optional

import typer
from rich.console import Console

from polyharmonics import __version__
from polyharmonics.cli import (
    associated_legendre_command,
    benchmark,
    legendre_command,
    spherical_harmonic_command,
)

app = typer.Typer(
    name="polyharmonics",
    help="Ortogonal Polynomials in the unit sphere.",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]polyharmonics[/] version: [bold blue]{__version__}[/]")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the polyharmonics package.",
    ),
):
    pass


app.command(name="legendre")(legendre_command)
app.command(name="associated-legendre")(associated_legendre_command)
app.command(name="spherical-harmonic")(spherical_harmonic_command)
app.add_typer(benchmark, name="benchmark")


if __name__ == "__main__":
    app()
