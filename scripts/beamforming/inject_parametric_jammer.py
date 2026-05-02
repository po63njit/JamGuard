#!/usr/bin/env python3
from pathlib import Path
import argparse, json, shutil, math
import numpy as np

def cfile_samples(path: Path) -> int:
    return path.stat().st_size // 8  # complex64 = 8 bytes

def parse_freqs(text: str):
    return [float(x.strip()) for x in text.split(",") if x.strip()]

def make_base(kind, t, amp, fs, args, rng):
    if kind == "cw":
        return amp * np.exp(1j * 2*np.pi*args.offset_hz*t)

    if kind == "multitone":
        freqs = parse_freqs(args.multitone_hz)
        y = np.zeros_like(t, dtype=np.complex64)
        scale = amp / math.sqrt(len(freqs))
        for f in freqs:
            y += scale * np.exp(1j * 2*np.pi*f*t)
        return y

    if kind == "chirp":
        period = args.chirp_period_s
        f0 = args.chirp_start_hz
        f1 = args.chirp_stop_hz
        tm = np.mod(t, period)
        k = (f1 - f0) / period
        phase = 2*np.pi*(f0*tm + 0.5*k*tm*tm)
        return amp * np.exp(1j * phase)

    if kind == "wideband_noise":
        n = len(t)
        noise = (rng.standard_normal(n) + 1j*rng.standard_normal(n)).astype(np.complex64) / np.sqrt(2.0)
        return amp * noise

    if kind == "pulsed_cw":
        phase = 2*np.pi*args.offset_hz*t
        gate = (np.mod(t * args.pulse_rate_hz, 1.0) < args.pulse_duty).astype(np.float32)
        return amp * gate * np.exp(1j * phase)

    raise ValueError(f"Unsupported single-source jammer kind: {kind}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--sample-rate", type=float, required=True)
    ap.add_argument("--channels", type=int, default=5)
    ap.add_argument("--pattern", default="ch{}.cfile")
    ap.add_argument("--max-samples", type=int, default=0)
    ap.add_argument("--block-samples", type=int, default=2_000_000)
    ap.add_argument("--kind", choices=["cw", "multitone", "chirp", "wideband_noise", "pulsed_cw", "two_cw"], required=True)
    ap.add_argument("--amplitude", type=float, required=True)
    ap.add_argument("--offset-hz", type=float, default=1500.0)
    ap.add_argument("--phase-step-rad", type=float, default=np.pi/8)
    ap.add_argument("--second-offset-hz", type=float, default=-3500.0)
    ap.add_argument("--second-phase-step-rad", type=float, default=-np.pi/5)
    ap.add_argument("--multitone-hz", default="1500,-4200,8300,12500,-16000")
    ap.add_argument("--chirp-start-hz", type=float, default=-60000.0)
    ap.add_argument("--chirp-stop-hz", type=float, default=60000.0)
    ap.add_argument("--chirp-period-s", type=float, default=0.25)
    ap.add_argument("--pulse-rate-hz", type=float, default=20.0)
    ap.add_argument("--pulse-duty", type=float, default=0.25)
    ap.add_argument("--seed", type=int, default=110)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    in_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)

    if out_dir.exists():
        if args.force:
            shutil.rmtree(out_dir)
        else:
            raise SystemExit(f"Output exists: {out_dir}. Use --force.")
    out_dir.mkdir(parents=True, exist_ok=True)

    in_paths = [in_dir / args.pattern.format(ch) for ch in range(args.channels)]
    for p in in_paths:
        if not p.exists():
            raise SystemExit(f"Missing input file: {p}")

    available = min(cfile_samples(p) for p in in_paths)
    total = available if args.max_samples <= 0 else min(args.max_samples, available)

    rng = np.random.default_rng(args.seed)

    infiles = [open(p, "rb") for p in in_paths]
    outfiles = [open(out_dir / args.pattern.format(ch), "wb") for ch in range(args.channels)]

    try:
        done = 0
        while done < total:
            n = min(args.block_samples, total - done)
            t = (done + np.arange(n, dtype=np.float64)) / args.sample_rate

            if args.kind == "two_cw":
                b1 = np.exp(1j * 2*np.pi*args.offset_hz*t).astype(np.complex64)
                b2 = np.exp(1j * 2*np.pi*args.second_offset_hz*t).astype(np.complex64)
                scale = args.amplitude / np.sqrt(2.0)
            else:
                base = make_base(args.kind, t, args.amplitude, args.sample_rate, args, rng).astype(np.complex64)

            for ch in range(args.channels):
                x = np.fromfile(infiles[ch], dtype=np.complex64, count=n)
                if len(x) != n:
                    raise RuntimeError(f"Short read on channel {ch}")

                if args.kind == "two_cw":
                    jammer = scale * (
                        b1 * np.exp(1j * args.phase_step_rad * ch)
                        + b2 * np.exp(1j * args.second_phase_step_rad * ch)
                    )
                else:
                    jammer = base * np.exp(1j * args.phase_step_rad * ch)

                y = (x + jammer).astype(np.complex64)
                y.tofile(outfiles[ch])

            done += n
            if done % (20_000_000) < args.block_samples:
                print(f"processed_samples={done}/{total}", flush=True)

    finally:
        for f in infiles + outfiles:
            f.close()

    manifest = {
        "kind": args.kind,
        "sample_rate": args.sample_rate,
        "channels": args.channels,
        "samples": total,
        "duration_s": total / args.sample_rate,
        "amplitude": args.amplitude,
        "offset_hz": args.offset_hz,
        "phase_step_rad": args.phase_step_rad,
        "second_offset_hz": args.second_offset_hz if args.kind == "two_cw" else None,
        "second_phase_step_rad": args.second_phase_step_rad if args.kind == "two_cw" else None,
        "seed": args.seed,
    }

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
