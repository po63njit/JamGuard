#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from jamguard.gnss.config import make_file_signal_source_config

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-cfile', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--sample-rate', type=int, required=True)
    ap.add_argument('--channels-1c', type=int, default=8)
    a=ap.parse_args()
    out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(make_file_signal_source_config(str(Path(a.input_cfile).resolve()), a.sample_rate, a.channels_1c))
if __name__=='__main__': main()
