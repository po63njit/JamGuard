"""Core data models for JamGuard offline analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray


@dataclass(slots=True)
class CaptureMetadata:
    """Metadata required to interpret a coherent multi-channel capture."""

    sample_rate_hz: float
    center_frequency_hz: float
    array_radius_m: float
    num_channels: int
    channel_paths: list[Path]
    channel_labels: list[str]
    reference_channel: str = "ch0"
    output_dir: Path = Path("results")
    capture_id: str = "capture"
    notes: str = ""

    def validate(self) -> None:
        """Validate metadata consistency and required fields."""
        if self.num_channels <= 0:
            raise ValueError("num_channels must be > 0")
        if len(self.channel_paths) != self.num_channels:
            raise ValueError("channel_paths length must equal num_channels")
        if len(self.channel_labels) != self.num_channels:
            raise ValueError("channel_labels length must equal num_channels")
        if self.reference_channel not in self.channel_labels:
            raise ValueError("reference_channel must be in channel_labels")


@dataclass(slots=True)
class MultiChannelCapture:
    """In-memory coherent data with shape (channels, samples)."""

    metadata: CaptureMetadata
    data: NDArray[np.complex64]

    def __post_init__(self) -> None:
        self.metadata.validate()
        if self.data.ndim != 2:
            raise ValueError("data must be 2D with shape (channels, samples)")
        if self.data.shape[0] != self.metadata.num_channels:
            raise ValueError("data channel axis must match metadata.num_channels")

    @property
    def num_samples(self) -> int:
        return int(self.data.shape[1])

    def channel_index(self, label: str) -> int:
        return self.metadata.channel_labels.index(label)

    def channel(self, label: str) -> NDArray[np.complex64]:
        return self.data[self.channel_index(label)]


@dataclass(slots=True)
class ChannelMetrics:
    """Per-channel health and ranking metrics."""

    mean_power: dict[str, float]
    rms: dict[str, float]
    ranking: list[str]
    preview: dict[str, list[float]]


@dataclass(slots=True)
class CalibrationResult:
    """Estimated relative complex calibration terms."""

    reference_channel: str
    complex_gain_by_channel: dict[str, complex]
    phase_offset_rad_by_channel: dict[str, float]
    amplitude_scale_by_channel: dict[str, float]
    lag_samples_by_channel: dict[str, int]

    def to_jsonable(self) -> dict[str, Any]:
        """Return JSON-serializable representation."""
        serial_gain = {
            k: {"real": float(v.real), "imag": float(v.imag)}
            for k, v in self.complex_gain_by_channel.items()
        }
        d = asdict(self)
        d["complex_gain_by_channel"] = serial_gain
        return d

    @classmethod
    def from_jsonable(cls, payload: dict[str, Any]) -> "CalibrationResult":
        """Create a calibration result from JSON payload."""
        gain = {
            k: complex(v["real"], v["imag"])
            for k, v in payload["complex_gain_by_channel"].items()
        }
        return cls(
            reference_channel=payload["reference_channel"],
            complex_gain_by_channel=gain,
            phase_offset_rad_by_channel={k: float(v) for k, v in payload["phase_offset_rad_by_channel"].items()},
            amplitude_scale_by_channel={k: float(v) for k, v in payload["amplitude_scale_by_channel"].items()},
            lag_samples_by_channel={k: int(v) for k, v in payload["lag_samples_by_channel"].items()},
        )


@dataclass(slots=True)
class BeamformingResult:
    """Result of fixed beamforming operation."""

    azimuth_deg: float
    weights: NDArray[np.complex128]
    output: NDArray[np.complex64]
    input_mean_power: float
    output_mean_power: float
    metadata: dict[str, Any] = field(default_factory=dict)
