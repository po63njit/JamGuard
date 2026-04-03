"""Synthetic interferer injection for offline experiments."""

from __future__ import annotations

import numpy as np

from jamguard.data.models import MultiChannelCapture
from jamguard.geometry.uca import steering_vector_azimuth, uca_positions


def inject_tone_interferer(
    capture: MultiChannelCapture,
    tone_hz: float,
    amplitude: float,
    azimuth_deg: float,
    initial_phase_rad: float = 0.0,
) -> MultiChannelCapture:
    """Inject directional tone interferer into all channels using UCA steering."""
    md = capture.metadata
    n = capture.num_samples
    t = np.arange(n, dtype=np.float64) / md.sample_rate_hz
    base = amplitude * np.exp(1j * (2.0 * np.pi * tone_hz * t + initial_phase_rad))

    positions = uca_positions(md.num_channels, md.array_radius_m)
    spatial = steering_vector_azimuth(positions, md.center_frequency_hz, azimuth_deg)

    jammer = spatial[:, None] * base[None, :]
    mixed = (capture.data + jammer).astype(np.complex64)
    return MultiChannelCapture(metadata=md, data=mixed)
