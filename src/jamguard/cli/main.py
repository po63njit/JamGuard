"""Typer-like CLI scaffold implemented with argparse for zero extra deps."""

from __future__ import annotations

import argparse
from pathlib import Path

from jamguard.config.loader import load_experiment_config


def app() -> None:
    """Console script entrypoint."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jamguard", description="JamGuard offline analysis CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_stub(name: str, help_text: str):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--config", type=Path, required=False)
        p.set_defaults(func=run_stub)

    add_stub("inspect", "Inspect capture metadata and channel files")
    add_stub("summarize", "Run channel health summary")
    add_stub("plot-psd", "Generate PSD plots")
    add_stub("compare-channels", "Run channel coherence/correlation checks")
    add_stub("calibrate", "Estimate channel calibration terms")
    add_stub("beamform", "Run offline beamforming")
    add_stub("inject-jammer", "Inject synthetic jammer")
    add_stub("make-report", "Produce markdown report")
    return parser


def run_stub(args: argparse.Namespace) -> None:
    """Placeholder command handler."""
    if args.config:
        _ = load_experiment_config(args.config)
    raise NotImplementedError("CLI command scaffolded but not yet implemented.")


if __name__ == "__main__":
    app()
