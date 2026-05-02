from __future__ import annotations
import numpy as np

def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.abs(x) ** 2)))

def power_dbfs(x: np.ndarray, eps: float = 1e-12) -> float:
    return float(10 * np.log10(np.mean(np.abs(x) ** 2) + eps))

def peak_mag(x: np.ndarray) -> float:
    return float(np.max(np.abs(x)))

def count_invalid(x: np.ndarray) -> int:
    return int(np.count_nonzero(~np.isfinite(x)))

def summarize_channel(x: np.ndarray, fs: float) -> dict:
    n = len(x)
    return {"samples": n, "duration_s": n / fs, "rms": rms(x), "power_dbfs": power_dbfs(x), "peak_mag": peak_mag(x), "invalid": count_invalid(x)}
