"""Steering vector generation for array processing."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from jamguard.utils.constants import SPEED_OF_LIGHT_MPS


def azel_to_unit_vector(az_deg: float, el_deg: float) -> NDArray[np.float64]:
    """Convert azimuth/elevation angles to a 3D unit propagation vector."""
    az = np.deg2rad(az_deg)
    el = np.deg2rad(el_deg)
    return np.array([
        np.cos(el) * np.cos(az),
        np.cos(el) * np.sin(az),
        np.sin(el),
    ])


def steering_vector(
    positions_m: NDArray[np.float64],
    center_frequency_hz: float,
    az_deg: float,
    el_deg: float,
) -> NDArray[np.complex128]:
    """Generate narrowband steering vector for given direction."""
    k = 2.0 * np.pi * center_frequency_hz / SPEED_OF_LIGHT_MPS
    u = azel_to_unit_vector(az_deg, el_deg)
    phase = -k * positions_m @ u
    return np.exp(1j * phase)
