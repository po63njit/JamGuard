"""Beamforming steering wrappers."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from jamguard.geometry.uca import steering_vector_azimuth


def steering_vector(
    positions_m: NDArray[np.float64],
    center_frequency_hz: float,
    az_deg: float,
    el_deg: float = 0.0,
) -> NDArray[np.complex128]:
    """Backward-compatible steering vector API for planar UCA MVP."""
    if abs(el_deg) > 1e-9:
        raise NotImplementedError("MVP supports planar (el=0) steering only")
    return steering_vector_azimuth(positions_m, center_frequency_hz, az_deg)
