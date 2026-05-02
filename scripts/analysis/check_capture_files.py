#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from jamguard.workflow import check_capture_files

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--sample-rate', type=float, default=2_000_000)
    ap.add_argument('--channels', type=int, default=5)
    ap.add_argument('--pattern', default='ch{}.cfile')
    ap.add_argument('--max-samples', type=int, default=None)
    a=ap.parse_args()
    rows=check_capture_files(a.input, sample_rate=a.sample_rate, channels=a.channels, pattern=a.pattern, max_samples=a.max_samples) if 'check_capture_files'!='check_capture_files' else check_capture_files(a.input, channels=a.channels, pattern=a.pattern)
    out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2))

if __name__=='__main__':
    main()
