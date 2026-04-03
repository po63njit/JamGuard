"""Frequency-domain estimation utilities."""

from __future__ import annotations

import numpy as np
from scipy.signal import welch


def estimate_psd(iq: np.ndarray, sample_rate_hz: float, nperseg: int = 4096) -> tuple[np.ndarray, np.ndarray]:
    """Estimate PSD (dB) using Welch method."""
    f, pxx = welch(
        iq,
        fs=sample_rate_hz,
        nperseg=min(nperseg, len(iq)),
        return_onesided=False,
        scaling="density",
    )
    pxx_db = 10.0 * np.log10(np.maximum(pxx, 1e-20))
    order = np.argsort(f)
    return f[order], pxx_db[order]
