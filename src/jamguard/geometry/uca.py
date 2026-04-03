"""Uniform circular array geometry and steering utilities."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from jamguard.utils.constants import SPEED_OF_LIGHT_MPS


def wavelength_m(center_frequency_hz: float) -> float:
    """Compute wavelength from carrier frequency."""
    return SPEED_OF_LIGHT_MPS / center_frequency_hz


def uca_positions(num_elements: int, radius_m: float) -> NDArray[np.float64]:
    """Return UCA coordinates in meters with shape (N, 3)."""
    if num_elements < 2:
        raise ValueError("num_elements must be >=2")
    ang = np.linspace(0.0, 2.0 * np.pi, num_elements, endpoint=False)
    return np.column_stack((radius_m * np.cos(ang), radius_m * np.sin(ang), np.zeros(num_elements)))


def steering_vector_azimuth(
    positions_m: NDArray[np.float64], center_frequency_hz: float, azimuth_deg: float
) -> NDArray[np.complex128]:
    """Generate narrowband steering vector for planar azimuth (elevation=0)."""
    az = np.deg2rad(azimuth_deg)
    u = np.array([np.cos(az), np.sin(az), 0.0])
    k = 2.0 * np.pi / wavelength_m(center_frequency_hz)
    phase = -k * (positions_m @ u)
    return np.exp(1j * phase)


def steering_matrix_azimuths(
    positions_m: NDArray[np.float64], center_frequency_hz: float, azimuth_deg: NDArray[np.float64]
) -> NDArray[np.complex128]:
    """Stack steering vectors for multiple azimuths -> (num_az, num_channels)."""
    return np.vstack([
        steering_vector_azimuth(positions_m, center_frequency_hz, float(az)) for az in azimuth_deg
    ])
