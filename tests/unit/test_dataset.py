import numpy as np

from jamguard.data.models import CaptureMetadata, ChannelData, MultiChannelCapture


def test_multichannel_matrix_shape() -> None:
    metadata = CaptureMetadata(
        capture_id="x",
        sample_rate_hz=1.0,
        center_frequency_hz=1.0,
        channel_labels=["a", "b"],
        channel_paths=[],
    )
    channels = [
        ChannelData("a", np.ones(8, dtype=np.complex64), 1.0, 1.0),
        ChannelData("b", np.ones(8, dtype=np.complex64), 1.0, 1.0),
    ]
    capture = MultiChannelCapture(metadata=metadata, channels=channels)
    assert capture.as_matrix().shape == (2, 8)
