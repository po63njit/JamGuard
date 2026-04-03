#!/usr/bin/env python3
"""Run first calibration summary."""

from __future__ import annotations

import argparse

from jamguard.calibration.channel_calibration import estimate_channel_calibration
from jamguard.io.loader import load_capture_from_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    capture = load_capture_from_config(args.config)
    cal = estimate_channel_calibration(capture, capture.metadata.reference_channel)
    for ch, val in cal.phase_offset_rad_by_channel.items():
        print(f"{ch}: phase={val:.4f} rad lag={cal.lag_samples_by_channel[ch]}")


if __name__ == "__main__":
    main()
