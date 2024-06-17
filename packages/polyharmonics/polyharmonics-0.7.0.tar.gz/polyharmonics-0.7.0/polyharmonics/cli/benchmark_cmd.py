import typer

from polyharmonics.cli.benchmark import (
    associated_legendre_bench_command,
    legendre_bench_command,
    spherical_harmonic_bench_command,
)

app = typer.Typer(
    help="Benchmark the calculation of the functions given by this package.",
)

app.command(name="legendre")(legendre_bench_command)
app.command(name="associated-legendre")(associated_legendre_bench_command)
app.command(name="spherical-harmonic")(spherical_harmonic_bench_command)

if __name__ == "__main__":
    app()


@app.callback()
def main():
    pass
