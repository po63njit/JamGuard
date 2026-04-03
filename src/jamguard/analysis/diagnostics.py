"""Channel-health and quality diagnostics."""

from __future__ import annotations

import numpy as np

from jamguard.data.models import AnalysisResult, MultiChannelCapture


def channel_health_summary(capture: MultiChannelCapture) -> AnalysisResult:
    """Compute basic channel power metrics for quick health checks."""
    metrics = {
        f"{ch.label}_rms": float(np.sqrt(np.mean(np.abs(ch.iq) ** 2)))
        for ch in capture.channels
    }
    return AnalysisResult(name="channel_health", metrics=metrics)
