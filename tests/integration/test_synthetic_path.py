import numpy as np

from jamguard.analysis.synthetic import inject_tone_interferer
from jamguard.beamforming.algorithms import delay_and_sum_beamform
from jamguard.data.models import CaptureMetadata, MultiChannelCapture


def test_inject_and_beamform_shapes() -> None:
    md = CaptureMetadata(
        sample_rate_hz=2.4e6,
        center_frequency_hz=1_575_420_000.0,
        array_radius_m=0.076,
        num_channels=5,
        channel_paths=[],
        channel_labels=[f"ch{i}" for i in range(5)],
        reference_channel="ch0",
    )
    md.channel_paths = [md.output_dir / f"ch{i}.cf32" for i in range(5)]
    data = np.zeros((5, 2048), dtype=np.complex64)
    cap = MultiChannelCapture(metadata=md, data=data)
    jam = inject_tone_interferer(cap, tone_hz=100_000.0, amplitude=1.0, azimuth_deg=40.0)
    assert jam.data.shape == (5, 2048)
    beam = delay_and_sum_beamform(jam, azimuth_deg=0.0)
    assert beam.output.shape == (2048,)
