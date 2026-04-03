"""Load raw IQ capture files and produce in-memory objects."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from jamguard.data.models import CaptureMetadata, ChannelData, MultiChannelCapture


def load_cf32_file(path: Path) -> NDArray[np.complex64]:
    """Load interleaved complex64 IQ samples from disk."""
    # TODO: support alternate file layouts and endian checks.
    return np.fromfile(path, dtype=np.complex64)


def load_capture_from_cf32(metadata: CaptureMetadata) -> MultiChannelCapture:
    """Load one-file-per-channel coherent capture from CF32 files."""
    channels: list[ChannelData] = []
    for label, path in zip(metadata.channel_labels, metadata.channel_paths, strict=True):
        iq = load_cf32_file(path)
        channels.append(
            ChannelData(
                label=label,
                iq=iq,
                sample_rate_hz=metadata.sample_rate_hz,
                center_frequency_hz=metadata.center_frequency_hz,
            )
        )
    # TODO: verify start-time alignment metadata for simultaneous capture.
    return MultiChannelCapture(metadata=metadata, channels=channels)
