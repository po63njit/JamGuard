#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from jamguard.workflow import run_lcmv

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--metrics-csv', required=True)
    ap.add_argument('--sample-rate', type=float, default=2_000_000)
    ap.add_argument('--channels', type=int, default=5)
    ap.add_argument('--pattern', default='ch{}.cfile')
    ap.add_argument('--max-samples', type=int, default=None)
    ap.add_argument('--force', action='store_true')
    a=ap.parse_args()
    print(json.dumps(run_lcmv(a.input,a.output_dir,a.metrics_csv,a.sample_rate,channels=a.channels,pattern=a.pattern,max_samples=a.max_samples,force=a.force),indent=2))
if __name__=='__main__': main()
