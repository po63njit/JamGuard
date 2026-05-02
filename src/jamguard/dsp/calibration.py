from __future__ import annotations
import numpy as np

def estimate_phase_correction(x_ref: np.ndarray, x: np.ndarray) -> complex:
    ph = np.angle(np.vdot(x, x_ref))
    return np.exp(1j * ph)

def estimate_all_phase_corrections(X: np.ndarray, ref_ch: int = 0) -> np.ndarray:
    c = np.ones(X.shape[0], dtype=np.complex64)
    for ch in range(X.shape[0]):
        if ch!=ref_ch:
            c[ch]=estimate_phase_correction(X[ref_ch],X[ch])
    return c

def apply_phase_corrections(X: np.ndarray, corrections: np.ndarray) -> np.ndarray:
    return X * corrections[:, None]
