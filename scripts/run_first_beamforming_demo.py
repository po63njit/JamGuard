#!/usr/bin/env python3
"""Run first beamforming demo with synthetic jammer."""

from __future__ import annotations

import argparse

from jamguard.analysis.synthetic import inject_tone_interferer
from jamguard.beamforming.algorithms import delay_and_sum_beamform
from jamguard.io.loader import load_capture_from_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--tone-hz", type=float, default=100_000.0)
    parser.add_argument("--amplitude", type=float, default=3.0)
    parser.add_argument("--jammer-azimuth-deg", type=float, default=60.0)
    parser.add_argument("--look-azimuth-deg", type=float, default=0.0)
    args = parser.parse_args()

    capture = load_capture_from_config(args.config)
    jammed = inject_tone_interferer(capture, args.tone_hz, args.amplitude, args.jammer_azimuth_deg)
    beam = delay_and_sum_beamform(jammed, args.look_azimuth_deg)
    print(f"Input mean power: {beam.input_mean_power:.6e}")
    print(f"Output mean power: {beam.output_mean_power:.6e}")


if __name__ == "__main__":
    main()
