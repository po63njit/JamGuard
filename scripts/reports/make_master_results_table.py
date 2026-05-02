#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--run-name', required=True)
    ap.add_argument('--lcmv-metrics', required=True)
    ap.add_argument('--jam-manifest', required=True)
    ap.add_argument('--output', required=True)
    a=ap.parse_args()
    metrics = next(csv.DictReader(open(a.lcmv_metrics)))
    manifest = json.loads(Path(a.jam_manifest).read_text())
    row = {"run_name": a.run_name, **metrics, "jam_amp": manifest.get('amplitude'), "jam_offset_hz": manifest.get('offset_hz')}
    out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(row.keys())); w.writeheader(); w.writerow(row)
if __name__=='__main__': main()
