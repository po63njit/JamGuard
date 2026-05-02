#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from jamguard.workflow import coarse_lag

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-dir', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--sample-rate', type=float, required=True)
    ap.add_argument('--channels', type=int, default=5)
    ap.add_argument('--pattern', default='ch{}.cfile')
    ap.add_argument('--max-samples', type=int, default=None)
    a=ap.parse_args()
    rows=coarse_lag(a.input_dir, sample_rate=a.sample_rate, channels=a.channels, pattern=a.pattern, max_samples=a.max_samples)
    out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2))

if __name__=='__main__':
    main()
