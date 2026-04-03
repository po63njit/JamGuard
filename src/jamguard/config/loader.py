"""Load JamGuard configuration files."""

from __future__ import annotations

from pathlib import Path
import tomllib

import yaml

from jamguard.config.models import AppConfig


def _read_config(path: Path) -> dict:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text) or {}
    if suffix == ".toml":
        return tomllib.loads(text)
    raise ValueError(f"Unsupported config file type: {suffix}")


def load_app_config(path: Path) -> AppConfig:
    """Load configuration from YAML or TOML into :class:`AppConfig`."""
    raw = _read_config(path)
    cfg = AppConfig(
        sample_rate_hz=float(raw["sample_rate_hz"]),
        center_frequency_hz=float(raw["center_frequency_hz"]),
        array_radius_m=float(raw["array_radius_m"]),
        num_channels=int(raw.get("num_channels", 5)),
        channel_files=[Path(p) for p in raw["channel_files"]],
        channel_labels=list(raw.get("channel_labels", [f"ch{i}" for i in range(int(raw.get("num_channels", 5)))])),
        reference_channel=str(raw.get("reference_channel", "ch0")),
        output_dir=Path(raw.get("output_dir", "results")),
        capture_id=str(raw.get("capture_id", path.stem)),
        notes=str(raw.get("notes", "")),
    )
    if len(cfg.channel_files) != cfg.num_channels:
        raise ValueError("channel_files length must equal num_channels")
    if len(cfg.channel_labels) != cfg.num_channels:
        raise ValueError("channel_labels length must equal num_channels")
    return cfg
