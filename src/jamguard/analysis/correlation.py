"""Correlation/coherence analysis for channel comparison."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from jamguard.data.models import MultiChannelCapture


def normalized_cross_correlation(
    x: NDArray[np.complex64], y: NDArray[np.complex64], max_lag: int = 256
) -> tuple[NDArray[np.float64], NDArray[np.float64], int]:
    """Return normalized cross-correlation magnitude around zero lag and lag estimate."""
    x0 = x - np.mean(x)
    y0 = y - np.mean(y)
    corr = np.correlate(x0, np.conj(y0), mode="full")
    lags = np.arange(-len(x) + 1, len(x))
    denom = (np.linalg.norm(x0) * np.linalg.norm(y0)) + 1e-12
    corr_norm = corr / denom

    keep = np.abs(lags) <= max_lag
    lags_keep = lags[keep]
    mag_keep = np.abs(corr_norm[keep])
    est_lag = int(lags_keep[np.argmax(mag_keep)])
    return lags_keep.astype(np.float64), mag_keep.astype(np.float64), est_lag


def correlation_magnitude_matrix(capture: MultiChannelCapture) -> NDArray[np.float64]:
    """Compute |corrcoef| matrix for all channels."""
    x = capture.data
    n = x.shape[0]
    out = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            num = np.vdot(x[i], x[j])
            den = (np.linalg.norm(x[i]) * np.linalg.norm(x[j])) + 1e-12
            out[i, j] = float(np.abs(num / den))
    return out


def phase_difference_vector(
    capture: MultiChannelCapture, reference_label: str, window_len: int = 4096
) -> dict[str, float]:
    """Estimate relative phase offsets in radians over analysis window."""
    ref_i = capture.channel_index(reference_label)
    ref = capture.data[ref_i, :window_len]
    result: dict[str, float] = {}
    for i, label in enumerate(capture.metadata.channel_labels):
        x = capture.data[i, :window_len]
        c = np.vdot(ref, x)
        result[label] = float(np.angle(c))
    return result
