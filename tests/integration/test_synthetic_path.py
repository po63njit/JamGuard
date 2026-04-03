import numpy as np

from jamguard.analysis.synthetic import inject_tone_interferer
from jamguard.data.models import CaptureMetadata, ChannelData, MultiChannelCapture


def test_inject_tone_changes_signal() -> None:
    metadata = CaptureMetadata(
        capture_id="synthetic",
        sample_rate_hz=10.0,
        center_frequency_hz=1.0,
        channel_labels=["ch0"],
        channel_paths=[],
    )
    ch = ChannelData("ch0", np.zeros(64, dtype=np.complex64), 10.0, 1.0)
    cap = MultiChannelCapture(metadata=metadata, channels=[ch])
    out = inject_tone_interferer(cap, tone_hz=1.0, amplitude=1.0)
    assert np.any(np.abs(out.channels[0].iq) > 0)
