"""Null-steering placeholder routines."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def design_single_null_weights(
    desired_steering: NDArray[np.complex128],
    null_steering: NDArray[np.complex128],
) -> NDArray[np.complex128]:
    """Return weights that enforce one linear null constraint."""
    # TODO: expand to LCMV with multiple null constraints.
    p = null_steering[:, None]
    proj = np.eye(len(desired_steering), dtype=np.complex128) - p @ np.linalg.pinv(p)
    w = proj @ desired_steering
    return w / (np.linalg.norm(w) + 1e-12)
