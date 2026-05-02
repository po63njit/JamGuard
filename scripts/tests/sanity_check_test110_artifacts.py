#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, sys

REQUIRED_MANIFEST = ["kind", "sample_rate", "channels", "samples", "duration_s", "amplitude", "offset_hz", "phase_step_rad", "seed"]
REQUIRED_CSV = ["case_id", "jammer_kind", "amplitude", "branch", "tracking_events", "unique_prns", "nav_messages", "position_fix"]

ap=argparse.ArgumentParser()
ap.add_argument('--manifest', default='')
ap.add_argument('--csv', default='results/tables/test_110_robust_sweep_180s.csv')
ap.add_argument('--gitignore', default='.gitignore')
args=ap.parse_args()

ok=True
if args.manifest:
    data=json.loads(Path(args.manifest).read_text())
    miss=[k for k in REQUIRED_MANIFEST if k not in data]
    if miss:
        ok=False; print(f'Manifest missing keys: {miss}')

c=Path(args.csv)
if c.exists():
    with c.open() as f: header=next(csv.reader(f))
    miss=[k for k in REQUIRED_CSV if k not in header]
    if miss:
        ok=False; print(f'CSV missing columns: {miss}')

ig=Path(args.gitignore).read_text()
for pat in ['*.cfile','results/packages/','pvt.dat_*.geojson']:
    if pat not in ig:
        ok=False; print(f'.gitignore missing pattern: {pat}')

print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
