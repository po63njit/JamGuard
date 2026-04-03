"""Phase and delay estimation placeholders."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def estimate_delay_samples(x: NDArray[np.complex64], y: NDArray[np.complex64]) -> int:
    """Estimate integer sample delay via peak cross-correlation."""
    corr = np.correlate(x, y, mode="full")
    lag = int(np.argmax(np.abs(corr)) - (len(y) - 1))
    return lag


def estimate_mean_phase_offset(x: NDArray[np.complex64], y: NDArray[np.complex64]) -> float:
    """Estimate average phase offset between two aligned channels."""
    return float(np.angle(np.vdot(x, y)))
