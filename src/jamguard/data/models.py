"""Core data abstractions shared across analysis modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray


@dataclass(slots=True)
class CaptureMetadata:
    """Metadata for one simultaneous multichannel capture."""

    capture_id: str
    sample_rate_hz: float
    center_frequency_hz: float
    channel_labels: list[str]
    channel_paths: list[Path]
    timestamp_utc: str | None = None
    notes: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ChannelData:
    """IQ data and derived annotations for one channel."""

    label: str
    iq: NDArray[np.complex64]
    sample_rate_hz: float
    center_frequency_hz: float


@dataclass(slots=True)
class MultiChannelCapture:
    """Container that binds channel data and shared metadata."""

    metadata: CaptureMetadata
    channels: list[ChannelData]

    def as_matrix(self) -> NDArray[np.complex64]:
        """Return stacked channel matrix with shape (num_channels, num_samples)."""
        if not channels_have_equal_length(self.channels):
            raise ValueError("All channels must have equal length.")
        return np.vstack([ch.iq for ch in self.channels]).astype(np.complex64)


@dataclass(slots=True)
class AnalysisResult:
    """Generic analysis result object for diagnostics/reporting."""

    name: str
    metrics: dict[str, float]
    artifacts: dict[str, Path] = field(default_factory=dict)


@dataclass(slots=True)
class CalibrationResult:
    """Per-channel calibration estimate."""

    reference_channel: str
    phase_offsets_rad: dict[str, float]
    delay_offsets_s: dict[str, float]
    amplitude_scales: dict[str, float]


@dataclass(slots=True)
class BeamformingResult:
    """Output of a beamforming operation."""

    output_signal: NDArray[np.complex64]
    weights: NDArray[np.complex128]
    metadata: dict[str, Any] = field(default_factory=dict)


def channels_have_equal_length(channels: list[ChannelData]) -> bool:
    """Return True when all channel vectors have the same number of samples."""
    return len({len(ch.iq) for ch in channels}) <= 1
