"""Jammer suppression and quality metrics."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def suppression_db(before: NDArray[np.complex64], after: NDArray[np.complex64]) -> float:
    """Return output suppression in dB using mean power ratio."""
    p_before = np.mean(np.abs(before) ** 2) + 1e-12
    p_after = np.mean(np.abs(after) ** 2) + 1e-12
    return float(10.0 * np.log10(p_before / p_after))
