"""Data loading helpers for CF32 multi-channel recordings."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from jamguard.config.loader import load_app_config
from jamguard.data.models import MultiChannelCapture

logger = logging.getLogger(__name__)


def load_cf32_file(path: Path) -> NDArray[np.complex64]:
    """Load complex64 IQ samples from a single channel file."""
    if not path.exists():
        raise FileNotFoundError(f"Channel file not found: {path}")
    iq = np.fromfile(path, dtype=np.complex64)
    if iq.size == 0:
        raise ValueError(f"Empty CF32 file: {path}")
    return iq


def load_capture_from_config(config_path: Path) -> MultiChannelCapture:
    """Load coherent multichannel capture using app config."""
    cfg = load_app_config(config_path)
    metadata = cfg.to_capture_metadata(config_path.parent)

    channels = [load_cf32_file(p) for p in metadata.channel_paths]
    lengths = [len(ch) for ch in channels]
    if len(set(lengths)) != 1:
        raise ValueError(f"Mismatched channel lengths: {lengths}")

    matrix = np.vstack(channels).astype(np.complex64)
    logger.info("Loaded %d channels, %d samples/channel", matrix.shape[0], matrix.shape[1])
    return MultiChannelCapture(metadata=metadata, data=matrix)
