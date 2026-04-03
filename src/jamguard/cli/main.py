"""JamGuard command-line interface."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from jamguard.analysis.correlation import correlation_magnitude_matrix, phase_difference_vector
from jamguard.analysis.diagnostics import compute_channel_metrics, metrics_table_text
from jamguard.analysis.synthetic import inject_tone_interferer
from jamguard.beamforming.algorithms import delay_and_sum_beamform
from jamguard.calibration.channel_calibration import (
    apply_calibration,
    estimate_channel_calibration,
    load_calibration_json,
    save_calibration_json,
)
from jamguard.io.loader import load_capture_from_config
from jamguard.plotting.figures import (
    plot_beam_pattern,
    plot_before_after_psd,
    plot_channel_power,
    plot_channel_psd,
    plot_correlation_heatmap,
    plot_phase_offsets,
)
from jamguard.reporting.reporting import write_json_summary
from jamguard.utils.logging_utils import configure_logging

logger = logging.getLogger(__name__)


def app() -> None:
    parser = build_parser()
    args = parser.parse_args()
    configure_logging()
    args.func(args)


def _load(args: argparse.Namespace):
    return load_capture_from_config(Path(args.config))


def cmd_inspect(args: argparse.Namespace) -> None:
    capture = _load(args)
    metrics = compute_channel_metrics(capture)
    print(metrics_table_text(metrics))


def cmd_plot_psd(args: argparse.Namespace) -> None:
    capture = _load(args)
    out = capture.metadata.output_dir / "psd_comparison.png"
    plot_channel_psd(capture, out)
    print(out)


def cmd_compare(args: argparse.Namespace) -> None:
    capture = _load(args)
    corr = correlation_magnitude_matrix(capture)
    phase = phase_difference_vector(capture, capture.metadata.reference_channel)
    out_dir = capture.metadata.output_dir
    plot_correlation_heatmap(corr, capture.metadata.channel_labels, out_dir / "correlation_heatmap.png")
    plot_phase_offsets(phase, out_dir / "phase_offsets.png")
    summary = {"correlation_matrix": corr.tolist(), "phase_offsets_rad": phase}
    write_json_summary(summary, out_dir / "compare_channels_summary.json")
    print(out_dir)


def cmd_calibrate(args: argparse.Namespace) -> None:
    capture = _load(args)
    cal = estimate_channel_calibration(capture, capture.metadata.reference_channel)
    out = capture.metadata.output_dir / "calibration.json"
    save_calibration_json(cal, out)
    plot_phase_offsets(cal.phase_offset_rad_by_channel, capture.metadata.output_dir / "calibration_phase_offsets.png")
    print(out)


def cmd_beamform(args: argparse.Namespace) -> None:
    capture = _load(args)
    if args.calibration:
        cal = load_calibration_json(Path(args.calibration))
        capture = apply_calibration(capture, cal)
    beam = delay_and_sum_beamform(capture, args.azimuth_deg)
    out_dir = capture.metadata.output_dir
    plot_before_after_psd(capture, beam, out_dir / "beamforming_before_after_psd.png")
    plot_beam_pattern(beam.weights, capture, out_dir / "beam_pattern.png")
    npy_path = out_dir / "beamformed_output.npy"
    import numpy as np

    np.save(npy_path, beam.output)
    write_json_summary(
        {
            "azimuth_deg": beam.azimuth_deg,
            "input_mean_power": beam.input_mean_power,
            "output_mean_power": beam.output_mean_power,
        },
        out_dir / "beamforming_summary.json",
    )
    print(npy_path)


def cmd_inject_jammer(args: argparse.Namespace) -> None:
    capture = _load(args)
    jammed = inject_tone_interferer(
        capture,
        tone_hz=args.tone_hz,
        amplitude=args.amplitude,
        azimuth_deg=args.azimuth_deg,
        initial_phase_rad=args.phase_rad,
    )
    out = jammed.metadata.output_dir / "jammed_capture.npy"
    import numpy as np

    np.save(out, jammed.data)
    print(out)


def cmd_demo(args: argparse.Namespace) -> None:
    capture = _load(args)
    metrics = compute_channel_metrics(capture)
    out_dir = capture.metadata.output_dir
    plot_channel_power(metrics, out_dir / "channel_power.png")
    plot_channel_psd(capture, out_dir / "psd_comparison.png")

    jammed = inject_tone_interferer(capture, args.tone_hz, args.amplitude, args.jammer_azimuth_deg)
    beam = delay_and_sum_beamform(jammed, args.look_azimuth_deg)

    corr = correlation_magnitude_matrix(jammed)
    cal = estimate_channel_calibration(jammed, jammed.metadata.reference_channel)

    plot_correlation_heatmap(corr, jammed.metadata.channel_labels, out_dir / "correlation_heatmap.png")
    plot_phase_offsets(cal.phase_offset_rad_by_channel, out_dir / "phase_offsets.png")
    plot_beam_pattern(beam.weights, jammed, out_dir / "beam_pattern.png")
    plot_before_after_psd(jammed, beam, out_dir / "beamforming_before_after_psd.png")

    write_json_summary(
        {
            "channel_mean_power": metrics.mean_power,
            "ranking": metrics.ranking,
            "jammer": {
                "tone_hz": args.tone_hz,
                "amplitude": args.amplitude,
                "jammer_azimuth_deg": args.jammer_azimuth_deg,
            },
            "beamforming": {
                "look_azimuth_deg": args.look_azimuth_deg,
                "input_mean_power": beam.input_mean_power,
                "output_mean_power": beam.output_mean_power,
            },
            "correlation_matrix": corr.tolist(),
        },
        out_dir / "demo_summary.json",
    )
    logger.info("Demo pipeline complete: %s", out_dir)
    print(out_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jamguard", description="JamGuard offline analysis CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("inspect", help="Channel health summary")
    p.add_argument("--config", required=True)
    p.set_defaults(func=cmd_inspect)

    p = sub.add_parser("plot-psd", help="Generate per-channel PSD plot")
    p.add_argument("--config", required=True)
    p.set_defaults(func=cmd_plot_psd)

    p = sub.add_parser("compare-channels", help="Correlation and phase comparison")
    p.add_argument("--config", required=True)
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser("calibrate", help="Estimate and save calibration")
    p.add_argument("--config", required=True)
    p.set_defaults(func=cmd_calibrate)

    p = sub.add_parser("beamform", help="Run fixed beamforming")
    p.add_argument("--config", required=True)
    p.add_argument("--azimuth-deg", type=float, default=0.0)
    p.add_argument("--calibration", type=str, default="")
    p.set_defaults(func=cmd_beamform)

    p = sub.add_parser("inject-jammer", help="Inject synthetic jammer")
    p.add_argument("--config", required=True)
    p.add_argument("--tone-hz", type=float, default=100_000.0)
    p.add_argument("--amplitude", type=float, default=3.0)
    p.add_argument("--azimuth-deg", type=float, default=45.0)
    p.add_argument("--phase-rad", type=float, default=0.0)
    p.set_defaults(func=cmd_inject_jammer)

    p = sub.add_parser("demo-pipeline", help="End-to-end first anti-jam demo")
    p.add_argument("--config", required=True)
    p.add_argument("--tone-hz", type=float, default=100_000.0)
    p.add_argument("--amplitude", type=float, default=3.0)
    p.add_argument("--jammer-azimuth-deg", type=float, default=60.0)
    p.add_argument("--look-azimuth-deg", type=float, default=0.0)
    p.set_defaults(func=cmd_demo)

    return parser


if __name__ == "__main__":
    app()
