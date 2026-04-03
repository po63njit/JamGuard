"""Classical beamforming algorithm placeholders."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from jamguard.data.models import BeamformingResult


def delay_and_sum(signal_matrix: NDArray[np.complex64], weights: NDArray[np.complex128]) -> BeamformingResult:
    """Apply fixed complex weights and sum channels."""
    output = weights.conj() @ signal_matrix
    return BeamformingResult(output_signal=output.astype(np.complex64), weights=weights)


def mvdr_placeholder(signal_matrix: NDArray[np.complex64], steering: NDArray[np.complex128]) -> BeamformingResult:
    """MVDR placeholder for future adaptive beamforming implementation."""
    # TODO: compute covariance matrix and apply MVDR weights.
    weights = steering / (np.linalg.norm(steering) + 1e-12)
    return delay_and_sum(signal_matrix, weights)
