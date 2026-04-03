import numpy as np

from jamguard.data.models import CaptureMetadata, MultiChannelCapture


def test_multichannel_shape() -> None:
    md = CaptureMetadata(
        sample_rate_hz=1.0,
        center_frequency_hz=1.0,
        array_radius_m=0.1,
        num_channels=5,
        channel_paths=[],
        channel_labels=[f"ch{i}" for i in range(5)],
        reference_channel="ch0",
    )
    md.channel_paths = [md.output_dir / f"ch{i}.cf32" for i in range(5)]
    data = np.zeros((5, 128), dtype=np.complex64)
    cap = MultiChannelCapture(metadata=md, data=data)
    assert cap.num_samples == 128
