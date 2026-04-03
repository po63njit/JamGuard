"""Configuration models for offline JamGuard runs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jamguard.data.models import CaptureMetadata


@dataclass(slots=True)
class AppConfig:
    """Top-level configuration parsed from YAML/TOML."""

    sample_rate_hz: float
    center_frequency_hz: float
    array_radius_m: float
    num_channels: int
    channel_files: list[Path]
    channel_labels: list[str]
    reference_channel: str
    output_dir: Path
    capture_id: str = "capture"
    notes: str = ""

    def to_capture_metadata(self, base_dir: Path) -> CaptureMetadata:
        """Build capture metadata with resolved channel paths."""
        resolved_files = [
            (p if p.is_absolute() else (base_dir / p)).resolve() for p in self.channel_files
        ]
        output_dir = self.output_dir if self.output_dir.is_absolute() else (base_dir / self.output_dir)
        return CaptureMetadata(
            sample_rate_hz=self.sample_rate_hz,
            center_frequency_hz=self.center_frequency_hz,
            array_radius_m=self.array_radius_m,
            num_channels=self.num_channels,
            channel_paths=resolved_files,
            channel_labels=self.channel_labels,
            reference_channel=self.reference_channel,
            output_dir=output_dir.resolve(),
            capture_id=self.capture_id,
            notes=self.notes,
        )
