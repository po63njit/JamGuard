"""Dataset helpers around capture configuration files."""

from __future__ import annotations

from pathlib import Path

from jamguard.io.loader import load_capture_from_config


class CaptureDataset:
    """Repository-style accessor for capture configs on disk."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def load_capture(self, config_path: Path):
        """Load one capture described by config file."""
        full = config_path if config_path.is_absolute() else self.root / config_path
        return load_capture_from_config(full)
