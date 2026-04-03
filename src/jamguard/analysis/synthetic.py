"""Synthetic jammer/interferer injection helpers."""

from __future__ import annotations

import numpy as np

from jamguard.data.models import MultiChannelCapture


def inject_tone_interferer(capture: MultiChannelCapture, tone_hz: float, amplitude: float) -> MultiChannelCapture:
    """Inject a shared complex tone interferer into all channels."""
    fs = capture.metadata.sample_rate_hz
    n = len(capture.channels[0].iq)
    t = np.arange(n) / fs
    tone = amplitude * np.exp(1j * 2.0 * np.pi * tone_hz * t).astype(np.complex64)
    for ch in capture.channels:
        ch.iq = (ch.iq + tone).astype(np.complex64)
    return capture
