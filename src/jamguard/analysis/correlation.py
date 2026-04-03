"""Correlation and coherence analysis utilities."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def complex_correlation(x: NDArray[np.complex64], y: NDArray[np.complex64]) -> complex:
    """Return normalized complex correlation coefficient."""
    num = np.vdot(x, y)
    den = np.sqrt(np.vdot(x, x).real * np.vdot(y, y).real) + 1e-12
    return complex(num / den)
