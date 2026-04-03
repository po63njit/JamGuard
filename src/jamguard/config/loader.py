"""Load JamGuard configuration from YAML/TOML files."""

from __future__ import annotations

from pathlib import Path
import tomllib

import yaml

from jamguard.config.models import ExperimentConfig


def load_experiment_config(path: Path) -> ExperimentConfig:
    """Load an :class:`ExperimentConfig` from YAML or TOML."""
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        raw = yaml.safe_load(text) or {}
    elif suffix == ".toml":
        raw = tomllib.loads(text)
    else:
        raise ValueError(f"Unsupported config type: {suffix}")

    return ExperimentConfig(
        name=raw.get("name", path.stem),
        description=raw.get("description", ""),
    )
