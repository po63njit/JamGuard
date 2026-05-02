#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jamguard.workflow import run_lcmv


def _resolve_sample_rate(input_dir: Path, sample_rate: float | None) -> float:
    if sample_rate is not None:
        return sample_rate
    manifest = input_dir / "manifest.json"
    if manifest.exists():
        meta = json.loads(manifest.read_text())
        if "sample_rate" in meta:
            return float(meta["sample_rate"])
    capture_meta = input_dir / "capture_metadata.json"
    if capture_meta.exists():
        meta = json.loads(capture_meta.read_text())
        if "sample_rate" in meta:
            return float(meta["sample_rate"])
    raise ValueError("sample rate required: pass --sample-rate or provide manifest metadata with sample_rate")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--metrics-csv', required=True)
    ap.add_argument('--sample-rate', type=float, default=None)
    ap.add_argument('--channels', type=int, default=5)
    ap.add_argument('--pattern', default='ch{}.cfile')
    ap.add_argument('--max-samples', type=int, default=None)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    sample_rate = _resolve_sample_rate(Path(a.input_dir), a.sample_rate)
    print(json.dumps(run_lcmv(a.input_dir, a.output_dir, a.metrics_csv, sample_rate, channels=a.channels, pattern=a.pattern, max_samples=a.max_samples, force=a.force), indent=2))


if __name__ == '__main__':
    main()
