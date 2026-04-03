"""Uniform circular array geometry helpers."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def uca_positions(num_elements: int, radius_m: float) -> NDArray[np.float64]:
    """Return Cartesian coordinates (N, 3) for a planar UCA centered at origin."""
    angles = np.linspace(0.0, 2.0 * np.pi, num_elements, endpoint=False)
    x = radius_m * np.cos(angles)
    y = radius_m * np.sin(angles)
    z = np.zeros_like(x)
    return np.column_stack((x, y, z))
