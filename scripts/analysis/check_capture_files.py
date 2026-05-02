#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from jamguard.workflow import check_capture_files

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-dir', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--channels', type=int, default=5)
    ap.add_argument('--pattern', default='ch{}.cfile')
    a=ap.parse_args()
    rows=check_capture_files(a.input_dir, channels=a.channels, pattern=a.pattern)
    out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2))

if __name__=='__main__':
    main()
