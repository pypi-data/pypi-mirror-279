# type: ignore[attr-defined]
"""Ortogonal Polynomials in the unit sphere."""

from importlib import metadata as importlib_metadata

from .associated_legendre_functions import associated_legendre
from .legendre_polynomials import legendre
from .spherical_harmonics import spherical_harmonic


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


__version__: str = get_version()
