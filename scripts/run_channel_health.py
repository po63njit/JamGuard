#!/usr/bin/env python3
"""Run first channel health summary."""

from __future__ import annotations

import argparse

from jamguard.analysis.diagnostics import compute_channel_metrics, metrics_table_text
from jamguard.io.loader import load_capture_from_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    capture = load_capture_from_config(args.config)
    metrics = compute_channel_metrics(capture)
    print(metrics_table_text(metrics))


if __name__ == "__main__":
    main()
