"""Dataset loading/orchestration helpers around core data models."""

from __future__ import annotations

from pathlib import Path

from jamguard.data.models import CaptureMetadata, MultiChannelCapture
from jamguard.io.loader import load_capture_from_cf32


class CaptureDataset:
    """Repository-style accessor for capture files on disk."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def load_cf32_capture(self, metadata: CaptureMetadata) -> MultiChannelCapture:
        """Load one capture described by metadata."""
        # TODO: add lazy loading/chunking for large captures.
        return load_capture_from_cf32(metadata)
