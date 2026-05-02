from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt

FS = 2_400_000.0
PROC_ROOT = Path("/media/patryk/X31/jamguard_processed_test110")
OUT_DIR = Path("results/tables")
FIG_DIR = Path("results/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

RUN_NAME = "test_110"
KINDS = ["cw", "chirp", "wideband_noise"]
AMPS = [3, 8, 16]

NFFT = 262_144
WINDOWS_PER_FILE = 8
TONE_HZ = 1500.0

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

def psd_metrics(path):
    n_samples = sample_count(path)
    starts = window_starts(n_samples, NFFT, WINDOWS_PER_FILE)

    win = np.hanning(NFFT).astype(np.float32)
    freqs = np.fft.fftshift(np.fft.fftfreq(NFFT, d=1.0 / FS))

    psd_acc = None
    time_powers = []

    for start in starts:
        x = read_window(path, start, NFFT)
        if len(x) != NFFT:
            continue

        x = x.astype(np.complex64)
        time_powers.append(float(np.mean(np.abs(x) ** 2)))

        x = x - np.mean(x)
        X = np.fft.fftshift(np.fft.fft(x * win))
        psd = (np.abs(X) ** 2) / np.sum(win ** 2)

        if psd_acc is None:
            psd_acc = psd
        else:
            psd_acc += psd

    psd_avg = psd_acc / len(starts)

    def band_mean_db(f_lo, f_hi):
        m = (freqs >= f_lo) & (freqs <= f_hi)
        return db(np.mean(psd_avg[m]))

    tone_idx = int(np.argmin(np.abs(freqs - TONE_HZ)))

    return {
        "samples": n_samples,
        "duration_s": n_samples / FS,
        "window_count": len(starts),
        "time_power_db": db(np.mean(time_powers)),
        "rms": float(np.sqrt(np.mean(time_powers))),
        "tone_1500_db": db(psd_avg[tone_idx]),
        "band_1500_pm5k_db": band_mean_db(TONE_HZ - 5_000, TONE_HZ + 5_000),
        "baseband_pm50k_db": band_mean_db(-50_000, 50_000),
        "wide_pm500k_db": band_mean_db(-500_000, 500_000),
        "fullband_avg_psd_db": db(np.mean(psd_avg)),
        "max_psd_db": db(np.max(psd_avg)),
        "median_psd_db": db(np.median(psd_avg)),
    }

rows = []

for kind in KINDS:
    for amp in AMPS:
        case_id = f"{RUN_NAME}_{kind}_amp{amp}_180s"
        jammed = PROC_ROOT / f"{case_id}_synth" / "ch0.cfile"
        lcmv = PROC_ROOT / f"{case_id}_lcmv" / "lcmv_ch0ref_null.cfile"

        if not jammed.exists() or not lcmv.exists():
            print(f"missing files for {case_id}")
            continue

        print(f"Analyzing {case_id}")
        b = psd_metrics(jammed)
        a = psd_metrics(lcmv)

        row = {
            "case_id": case_id,
            "jammer_kind": kind,
            "amplitude": amp,
            "duration_s": round(a["duration_s"], 3),

            "jammed_time_power_db": round(b["time_power_db"], 3),
            "lcmv_time_power_db": round(a["time_power_db"], 3),
            "time_power_reduction_db": round(b["time_power_db"] - a["time_power_db"], 3),

            "jammed_tone_1500_db": round(b["tone_1500_db"], 3),
            "lcmv_tone_1500_db": round(a["tone_1500_db"], 3),
            "tone_1500_suppression_db": round(b["tone_1500_db"] - a["tone_1500_db"], 3),

            "band_1500_pm5k_suppression_db": round(b["band_1500_pm5k_db"] - a["band_1500_pm5k_db"], 3),
            "baseband_pm50k_suppression_db": round(b["baseband_pm50k_db"] - a["baseband_pm50k_db"], 3),
            "wide_pm500k_suppression_db": round(b["wide_pm500k_db"] - a["wide_pm500k_db"], 3),
            "fullband_avg_psd_reduction_db": round(b["fullband_avg_psd_db"] - a["fullband_avg_psd_db"], 3),

            "jammed_max_psd_db": round(b["max_psd_db"], 3),
            "lcmv_max_psd_db": round(a["max_psd_db"], 3),
            "max_psd_reduction_db": round(b["max_psd_db"] - a["max_psd_db"], 3),

            "lcmv_rms": round(a["rms"], 6),
            "windows_per_file": a["window_count"],
        }

        if kind == "cw":
            row["primary_metric"] = "tone_1500_suppression_db"
            row["primary_suppression_db"] = row["tone_1500_suppression_db"]
        elif kind == "chirp":
            row["primary_metric"] = "wide_pm500k_suppression_db"
            row["primary_suppression_db"] = row["wide_pm500k_suppression_db"]
        else:
            row["primary_metric"] = "fullband_avg_psd_reduction_db"
            row["primary_suppression_db"] = row["fullband_avg_psd_reduction_db"]

        rows.append(row)

csv_path = OUT_DIR / "test_110_robust_spectral_metrics.csv"
with csv_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

md_path = OUT_DIR / "test_110_robust_spectral_metrics.md"
with md_path.open("w") as f:
    f.write("# test_110 robust synthetic jammer spectral metrics\n\n")
    f.write("These metrics compare the jammed CH0 stream against the LCMV beamformed output for each 180-second test case.\n\n")
    f.write("| Jammer | Amp | Primary metric | Primary suppression dB | Tone 1.5 kHz suppression dB | ±500 kHz suppression dB | Fullband PSD reduction dB | Time-power reduction dB |\n")
    f.write("|---|---:|---|---:|---:|---:|---:|---:|\n")
    for r in rows:
        f.write(
            f"| {r['jammer_kind']} | {r['amplitude']} | {r['primary_metric']} | "
            f"{r['primary_suppression_db']:.3f} | {r['tone_1500_suppression_db']:.3f} | "
            f"{r['wide_pm500k_suppression_db']:.3f} | {r['fullband_avg_psd_reduction_db']:.3f} | "
            f"{r['time_power_reduction_db']:.3f} |\n"
        )

labels = [f"{r['jammer_kind']}\namp {r['amplitude']}" for r in rows]
vals = [r["primary_suppression_db"] for r in rows]

plt.figure(figsize=(12, 5))
plt.bar(labels, vals)
plt.ylabel("Suppression / reduction (dB)")
plt.title("test_110 robust sweep primary suppression metric")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
fig_path = FIG_DIR / "test_110_robust_primary_suppression.png"
plt.savefig(fig_path, dpi=180)
plt.close()

print("Wrote:")
print(csv_path)
print(md_path)
print(fig_path)
