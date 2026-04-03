import numpy as np

from jamguard.calibration.channel_calibration import estimate_channel_calibration
from jamguard.data.models import CaptureMetadata, MultiChannelCapture


def test_basic_calibration_estimation() -> None:
    n = 4096
    ref = np.exp(1j * 2 * np.pi * 0.02 * np.arange(n)).astype(np.complex64)
    data = np.vstack([
        ref,
        (0.5 * np.exp(1j * 0.3) * ref).astype(np.complex64),
        (1.2 * np.exp(1j * -0.4) * ref).astype(np.complex64),
        ref,
        ref,
    ])
    md = CaptureMetadata(
        sample_rate_hz=1.0,
        center_frequency_hz=1.0,
        array_radius_m=0.076,
        num_channels=5,
        channel_paths=[],
        channel_labels=[f"ch{i}" for i in range(5)],
        reference_channel="ch0",
    )
    md.channel_paths = [md.output_dir / f"ch{i}.cf32" for i in range(5)]
    cap = MultiChannelCapture(metadata=md, data=data)
    cal = estimate_channel_calibration(cap, "ch0")
    assert "ch1" in cal.phase_offset_rad_by_channel
    assert len(cal.complex_gain_by_channel) == 5
