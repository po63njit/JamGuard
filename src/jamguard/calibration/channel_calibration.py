"""Channel calibration scaffolding."""

from __future__ import annotations

from jamguard.data.models import CalibrationResult, MultiChannelCapture


def estimate_channel_calibration(capture: MultiChannelCapture, reference_channel: str) -> CalibrationResult:
    """Estimate per-channel relative phase/delay/amplitude offsets."""
    # TODO: estimate per-channel phase offset from simultaneous captures.
    labels = [ch.label for ch in capture.channels]
    phase = {label: 0.0 for label in labels}
    delay = {label: 0.0 for label in labels}
    amp = {label: 1.0 for label in labels}
    return CalibrationResult(reference_channel=reference_channel, phase_offsets_rad=phase, delay_offsets_s=delay, amplitude_scales=amp)
