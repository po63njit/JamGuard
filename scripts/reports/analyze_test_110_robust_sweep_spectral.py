#!/usr/bin/env python3
from pathlib import Path
import argparse, csv
import numpy as np
import matplotlib.pyplot as plt


def db(x):
    return 10.0 * np.log10(float(x) + 1e-30)


def sample_count(path):
    return path.stat().st_size // np.dtype(np.complex64).itemsize


def read_window(path, start, count):
    with path.open("rb") as f:
        f.seek(start * np.dtype(np.complex64).itemsize)
        return np.fromfile(f, dtype=np.complex64, count=count)


def window_starts(n_samples, nfft, nwin):
    if n_samples <= nfft:
        return [0]
    return [int(x) for x in np.linspace(0, n_samples - nfft, nwin)]


def psd_metrics(path, fs, nfft, windows_per_file, tone_hz):
    n_samples = sample_count(path)
    starts = window_starts(n_samples, nfft, windows_per_file)
    win = np.hanning(nfft).astype(np.float32)
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft, d=1.0 / fs))

    psd_acc = None
    time_powers = []
    used = 0
    for start in starts:
        x = read_window(path, start, nfft)
        if len(x) != nfft:
            continue
        used += 1
        time_powers.append(float(np.mean(np.abs(x) ** 2)))
        X = np.fft.fftshift(np.fft.fft((x - np.mean(x)) * win))
        psd = (np.abs(X) ** 2) / np.sum(win ** 2)
        psd_acc = psd if psd_acc is None else psd_acc + psd

    if used == 0:
        raise RuntimeError(f"No full windows could be read from {path}")

    psd_avg = psd_acc / used
    tone_idx = int(np.argmin(np.abs(freqs - tone_hz)))

    def band_mean_db(f_lo, f_hi):
        m = (freqs >= f_lo) & (freqs <= f_hi)
        return db(np.mean(psd_avg[m]))

    return {
        "duration_s": n_samples / fs,
        "window_count": used,
        "time_power_db": db(np.mean(time_powers)),
        "rms": float(np.sqrt(np.mean(time_powers))),
        "tone_1500_db": db(psd_avg[tone_idx]),
        "band_1500_pm5k_db": band_mean_db(tone_hz - 5_000, tone_hz + 5_000),
        "baseband_pm50k_db": band_mean_db(-50_000, 50_000),
        "wide_pm500k_db": band_mean_db(-500_000, 500_000),
        "fullband_avg_psd_db": db(np.mean(psd_avg)),
        "max_psd_db": db(np.max(psd_avg)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proc-root", default="/media/patryk/X31/jamguard_processed_test110")
    ap.add_argument("--run-name", default="test_110")
    ap.add_argument("--kinds", default="cw,chirp,wideband_noise")
    ap.add_argument("--amps", default="3,8,16")
    ap.add_argument("--sample-rate", type=float, default=2_400_000.0)
    ap.add_argument("--nfft", type=int, default=262_144)
    ap.add_argument("--windows-per-file", type=int, default=8)
    ap.add_argument("--tone-hz", type=float, default=1500.0)
    ap.add_argument("--out-csv", default="results/tables/test_110_robust_spectral_metrics.csv")
    ap.add_argument("--out-md", default="results/tables/test_110_robust_spectral_metrics.md")
    ap.add_argument("--out-fig", default="results/figures/test_110_robust_primary_suppression.png")
    args = ap.parse_args()

    proc_root = Path(args.proc_root)
    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_fig).parent.mkdir(parents=True, exist_ok=True)
    kinds = [k.strip() for k in args.kinds.split(",") if k.strip()]
    amps = [float(a) for a in args.amps.split(",") if a.strip()]

    rows = []
    for kind in kinds:
        for amp in amps:
            amp_tag = str(int(amp)) if float(amp).is_integer() else str(amp).replace('.', 'p')
            case_id = f"{args.run_name}_{kind}_amp{amp_tag}_180s"
            jammed = proc_root / f"{case_id}_synth" / "ch0.cfile"
            lcmv = proc_root / f"{case_id}_lcmv" / "lcmv_ch0ref_null.cfile"
            if not jammed.exists() or not lcmv.exists():
                print(f"missing files for {case_id}")
                continue
            b = psd_metrics(jammed, args.sample_rate, args.nfft, args.windows_per_file, args.tone_hz)
            a = psd_metrics(lcmv, args.sample_rate, args.nfft, args.windows_per_file, args.tone_hz)
            row = {"case_id": case_id, "jammer_kind": kind, "amplitude": amp, "duration_s": round(a["duration_s"], 3),
                   "tone_1500_suppression_db": round(b["tone_1500_db"] - a["tone_1500_db"], 3),
                   "wide_pm500k_suppression_db": round(b["wide_pm500k_db"] - a["wide_pm500k_db"], 3),
                   "fullband_avg_psd_reduction_db": round(b["fullband_avg_psd_db"] - a["fullband_avg_psd_db"], 3),
                   "time_power_reduction_db": round(b["time_power_db"] - a["time_power_db"], 3)}
            row["primary_metric"] = "tone_1500_suppression_db" if kind == "cw" else ("wide_pm500k_suppression_db" if kind == "chirp" else "fullband_avg_psd_reduction_db")
            row["primary_suppression_db"] = row[row["primary_metric"]]
            rows.append(row)

    if not rows:
        raise SystemExit("No rows generated; check paths and case names.")

    with Path(args.out_csv).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    with Path(args.out_md).open("w") as f:
        f.write("# test_110 robust synthetic jammer spectral metrics\n\n")
        for r in rows:
            f.write(f"- {r['case_id']}: {r['primary_metric']}={r['primary_suppression_db']:.3f} dB\n")

    labels = [f"{r['jammer_kind']}\namp {r['amplitude']}" for r in rows]
    vals = [r["primary_suppression_db"] for r in rows]
    plt.figure(figsize=(12, 5)); plt.bar(labels, vals); plt.ylabel("Suppression / reduction (dB)"); plt.tight_layout(); plt.savefig(args.out_fig, dpi=180); plt.close()


if __name__ == "__main__":
    main()
