"""Configuration dataclasses for JamGuard experiments."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from jamguard.utils.constants import (
    DEFAULT_NUM_CHANNELS,
    DEFAULT_SAMPLE_RATE_HZ,
    GPS_L1_CENTER_HZ,
    UCA_DEFAULT_RADIUS_M,
)


@dataclass(slots=True)
class PathsConfig:
    data_root: Path = Path("data")
    results_root: Path = Path("results")


@dataclass(slots=True)
class ArrayConfig:
    geometry: str = "uca"
    num_elements: int = DEFAULT_NUM_CHANNELS
    radius_m: float = UCA_DEFAULT_RADIUS_M
    channel_labels: list[str] = field(default_factory=lambda: [f"ch{i}" for i in range(DEFAULT_NUM_CHANNELS)])


@dataclass(slots=True)
class SignalConfig:
    center_frequency_hz: float = GPS_L1_CENTER_HZ
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ


@dataclass(slots=True)
class CalibrationConfig:
    reference_channel: str = "ch0"
    method: str = "cross_correlation"


@dataclass(slots=True)
class BeamformingConfig:
    method: str = "delay_and_sum"
    look_az_deg: float = 0.0
    look_el_deg: float = 0.0


@dataclass(slots=True)
class ExperimentConfig:
    name: str
    description: str = ""
    paths: PathsConfig = field(default_factory=PathsConfig)
    array: ArrayConfig = field(default_factory=ArrayConfig)
    signal: SignalConfig = field(default_factory=SignalConfig)
    calibration: CalibrationConfig = field(default_factory=CalibrationConfig)
    beamforming: BeamformingConfig = field(default_factory=BeamformingConfig)
