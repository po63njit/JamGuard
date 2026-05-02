#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
from jamguard.io.cfile import write_complex64_cfile

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--sample-rate', type=float, default=2_000_000)
    ap.add_argument('--channels', type=int, default=5)
    ap.add_argument('--pattern', default='ch{}.cfile')
    ap.add_argument('--samples', type=int, default=4096)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    out = Path(a.output_dir)
    if out.exists() and any(out.iterdir()) and not a.force:
        raise FileExistsError(f'output exists, pass --force: {out}')
    out.mkdir(parents=True, exist_ok=True)
    t = np.arange(a.samples) / a.sample_rate
    for ch in range(a.channels):
        phase = ch * 0.2
        x = (0.7*np.exp(1j*(2*np.pi*25_000*t + phase)) + 0.05*np.exp(1j*(2*np.pi*2_000*t))).astype(np.complex64)
        write_complex64_cfile(out / a.pattern.format(ch), x)
    (out / 'capture_metadata.json').write_text(json.dumps({'sample_rate': a.sample_rate, 'channels': a.channels, 'samples': a.samples, 'phase_step_rad': 0.2}, indent=2))

if __name__ == '__main__':
    main()
