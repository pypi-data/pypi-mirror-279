from typing import List

import matplotlib.pyplot as plt
import numpy as np
import typer
from matplotlib import cm, colors
from rich.console import Console

# Assuming spherical_harmonic is already defined
from polyharmonics import spherical_harmonic

console = Console()


def plotsh_command(
    nm: str = typer.Argument(
        ...,
        help="""The corresponding subscript(s) and superscript(s) of the function(s).
        Either a pair of integers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
        metavar="SUB:SUP",
    ),
) -> None:
    """Plot the spherical harmonics given by this package."""

    try:
        n_values: List[int] = []
        m_values: List[int] = []
        for value in nm.split(","):
            n, m = value.split(":")
            if n is None or m is None or n == "" or m == "":
                raise typer.BadParameter(
                    "nm must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
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

    theta, phi = np.meshgrid(np.linspace(0, np.pi, 100), np.linspace(0, 2 * np.pi, 100))
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    for i, (n, m) in enumerate(zip(n_values, m_values)):
        fig = plt.figure(num=i + 1, figsize=(12, 12))
        ax = fig.add_subplot(111, projection="3d")
        Ynm_real = np.real(spherical_harmonic(n, m, th=theta, phi=phi))
        r = np.abs(Ynm_real)
        x_plot, y_plot, z_plot = r * x, r * y, r * z
        norm = colors.Normalize(vmin=-0.5, vmax=0.5)
        color_map = cm.ScalarMappable(norm=norm, cmap=cm.coolwarm)

        ax.plot_surface(
            x_plot,
            y_plot,
            z_plot,
            facecolors=color_map.to_rgba(Ynm_real),
            antialiased=True,
            shade=False,
        )
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title(f"Spherical Harmonic $Y_{'{' + str(n) + '}'}^{'{' + str(m) + '}'}$")

        color_bar = fig.colorbar(color_map, ax=ax, shrink=0.5, aspect=5, pad=0.1)
        color_bar.set_label("Real Part of Spherical Harmonic")

        plt.show()
    raise typer.Exit()
