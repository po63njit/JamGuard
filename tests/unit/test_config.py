from pathlib import Path

from jamguard.config.loader import load_app_config


def test_load_yaml_config(tmp_path: Path) -> None:
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(
        "\n".join(
            [
                "sample_rate_hz: 2400000",
                "center_frequency_hz: 1575420000",
                "array_radius_m: 0.076",
                "num_channels: 2",
                "channel_files: [ch0.cf32, ch1.cf32]",
                "channel_labels: [ch0, ch1]",
                "reference_channel: ch0",
                "output_dir: results",
            ]
        ),
        encoding="utf-8",
    )
    cfg = load_app_config(cfg_path)
    assert cfg.num_channels == 2
