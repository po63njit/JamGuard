#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from jamguard.io.cfile import read_complex64_cfile


def summarize_cfile(path: Path, sample_rate: float | None) -> dict:
    x = read_complex64_cfile(path)
    mag = np.abs(x)
    power = mag ** 2
    finite_mask = np.isfinite(x.real) & np.isfinite(x.imag)
    finite_mag = mag[finite_mask]
    finite_power = power[finite_mask]

    sample_count = int(x.shape[0])
    result = {
        "path": str(path),
        "sample_count": sample_count,
        "nan_inf_count": int((~finite_mask).sum()),
        "rms": float(np.sqrt(np.mean(finite_power))) if finite_power.size else float("nan"),
        "power": float(np.mean(finite_power)) if finite_power.size else float("nan"),
        "min_magnitude": float(finite_mag.min()) if finite_mag.size else float("nan"),
        "max_magnitude": float(finite_mag.max()) if finite_mag.size else float("nan"),
    }
    if sample_rate is not None:
        result["sample_rate"] = float(sample_rate)
        result["duration_seconds"] = sample_count / float(sample_rate)
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Inspect complex64 .cfile statistics")
    ap.add_argument("--input-cfile", required=True)
    ap.add_argument("--sample-rate", type=float, default=None)
    ap.add_argument("--output", default="")
    a = ap.parse_args()

    summary = summarize_cfile(Path(a.input_cfile), a.sample_rate)
    text = json.dumps(summary, indent=2)
    print(text)
    if a.output:
        out = Path(a.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n")


if __name__ == "__main__":
    main()
