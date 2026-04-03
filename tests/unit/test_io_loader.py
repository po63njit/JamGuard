import numpy as np

from jamguard.io.loader import load_capture_from_config


def test_load_cf32_set(tmp_path):
    n = 128
    for i in range(5):
        (np.ones(n, dtype=np.complex64) * (i + 1)).tofile(tmp_path / f"ch{i}.cf32")

    cfg = tmp_path / "cfg.yaml"
    cfg.write_text(
        "\n".join(
            [
                "sample_rate_hz: 2400000",
                "center_frequency_hz: 1575420000",
                "array_radius_m: 0.076",
                "num_channels: 5",
                "channel_files: [ch0.cf32, ch1.cf32, ch2.cf32, ch3.cf32, ch4.cf32]",
                "channel_labels: [ch0, ch1, ch2, ch3, ch4]",
                "reference_channel: ch0",
                "output_dir: results",
            ]
        ),
        encoding="utf-8",
    )
    cap = load_capture_from_config(cfg)
    assert cap.data.shape == (5, n)
