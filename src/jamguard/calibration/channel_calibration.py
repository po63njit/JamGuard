"""Basic offline relative channel calibration."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from jamguard.analysis.correlation import normalized_cross_correlation
from jamguard.data.models import CalibrationResult, MultiChannelCapture


def estimate_channel_calibration(
    capture: MultiChannelCapture,
    reference_channel: str,
    window_len: int = 32768,
) -> CalibrationResult:
    """Estimate per-channel complex gain terms relative to reference channel."""
    ref_i = capture.channel_index(reference_channel)
    ref = capture.data[ref_i, :window_len]

    gains: dict[str, complex] = {}
    phase: dict[str, float] = {}
    amp: dict[str, float] = {}
    lag: dict[str, int] = {}

    for i, label in enumerate(capture.metadata.channel_labels):
        x = capture.data[i, :window_len]
        g = np.vdot(ref, x) / (np.vdot(x, x) + 1e-12)
        gains[label] = complex(g)
        phase[label] = float(np.angle(g))
        amp[label] = float(np.abs(g))
        _, _, lag_est = normalized_cross_correlation(ref, x, max_lag=512)
        lag[label] = int(lag_est)

    return CalibrationResult(
        reference_channel=reference_channel,
        complex_gain_by_channel=gains,
        phase_offset_rad_by_channel=phase,
        amplitude_scale_by_channel=amp,
        lag_samples_by_channel=lag,
    )


def apply_calibration(capture: MultiChannelCapture, cal: CalibrationResult) -> MultiChannelCapture:
    """Apply inverse gain correction to each channel."""
    corrected = np.empty_like(capture.data)
    for i, label in enumerate(capture.metadata.channel_labels):
        g = cal.complex_gain_by_channel[label]
        corrected[i] = capture.data[i] / (g + 1e-12)
    return MultiChannelCapture(metadata=capture.metadata, data=corrected.astype(np.complex64))


def save_calibration_json(cal: CalibrationResult, path: Path) -> None:
    """Write calibration result to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cal.to_jsonable(), indent=2), encoding="utf-8")


def load_calibration_json(path: Path) -> CalibrationResult:
    """Load calibration result from disk."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    return CalibrationResult.from_jsonable(payload)
