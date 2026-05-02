from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(".")
TABLES = ROOT / "results" / "tables"
FIGS = ROOT / "results" / "figures"
PKG = ROOT / "results" / "packages"

TABLES.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)
PKG.mkdir(parents=True, exist_ok=True)

rows = [
    {
        "segment_s": 10,
        "samples": 24_000_000,
        "output_power_db": -23.02945777660208,
        "rms": 0.07055488973855972,
        "covariance_condition_number": 17970.39855054187,
        "jammer_bin_before_db": 67.26,
        "jammer_bin_after_db": -23.07,
        "jammer_suppression_db": 90.33,
        "gnss_tracking_events": 4,
        "unique_prns_tracked": 4,
        "nav_messages": 0,
        "position_fix": "No",
    },
    {
        "segment_s": 60,
        "samples": 144_000_000,
        "output_power_db": -18.43354440342396,
        "rms": 0.11976303160190582,
        "covariance_condition_number": 29955.022826151486,
        "jammer_bin_before_db": 72.91,
        "jammer_bin_after_db": -19.09,
        "jammer_suppression_db": 92.00,
        "gnss_tracking_events": 10,
        "unique_prns_tracked": 7,
        "nav_messages": 21,
        "position_fix": "No",
    },
    {
        "segment_s": 180,
        "samples": 432_000_000,
        "output_power_db": -21.97074520127338,
        "rms": 0.07970081269741058,
        "covariance_condition_number": 2023.7738135076092,
        "jammer_bin_before_db": 72.91,
        "jammer_bin_after_db": -24.27,
        "jammer_suppression_db": 97.18,
        "gnss_tracking_events": 11,
        "unique_prns_tracked": 8,
        "nav_messages": 119,
        "position_fix": "Yes",
    },
]

headers = list(rows[0].keys())

# CSV table
csv_path = TABLES / "test_110_packaged_results.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

def fmt(v):
    if isinstance(v, float):
        return f"{v:.3f}"
    return str(v)

def markdown_table(headers, rows):
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(fmt(r[h]) for h in headers) + " |")
    return "\n".join(out)

md = f"""# test_110 packaged anti-jam results

## Summary table

{markdown_table(headers, rows)}

## Lead result

The strongest result is the 180-second LCMV run:

- Processed samples: 432,000,000 complex64 samples
- Jammer-bin suppression: 97.18 dB
- GNSS-SDR tracking-start events: 11
- Unique GPS L1 C/A PRNs tracked: 8
- GPS NAV messages decoded: 119
- GNSS-SDR position fix: yes

## Report-safe conclusion

A real five-channel KrakenSDR GNSS capture was phase-aligned, injected with a controlled synthetic spatial narrowband jammer, processed through an LCMV/nulling beamformer, and exported as a GNSS-SDR-compatible complex64 stream.

In the 180-second run, the beamformer suppressed the injected jammer bin by approximately 97.2 dB while preserving enough GPS L1 C/A signal structure for GNSS-SDR to track multiple satellites, decode 119 NAV messages, and compute a position fix.

This should be presented as controlled synthetic narrowband spatial jammer suppression on real captured GNSS data, not as a claim of immunity against arbitrary real-world jamming or as a direct claim of outperforming commercial CRPA anti-jam systems.
"""

md_path = TABLES / "test_110_packaged_results.md"
md_path.write_text(md, encoding="utf-8")

segment_labels = [str(r["segment_s"]) for r in rows]

# Figure 1
plt.figure(figsize=(7, 4.5))
plt.bar(segment_labels, [r["jammer_suppression_db"] for r in rows])
plt.xlabel("Processed segment length (s)")
plt.ylabel("Jammer-bin suppression (dB)")
plt.title("test_110 jammer-bin suppression after LCMV nulling")
plt.tight_layout()
fig1 = FIGS / "test_110_jammer_suppression_vs_duration.png"
plt.savefig(fig1, dpi=200)
plt.close()

# Figure 2
x = np.arange(len(rows))
width = 0.25
plt.figure(figsize=(8, 4.8))
plt.bar(x - width, [r["gnss_tracking_events"] for r in rows], width, label="Tracking events")
plt.bar(x, [r["unique_prns_tracked"] for r in rows], width, label="Unique PRNs")
plt.bar(x + width, [r["nav_messages"] for r in rows], width, label="NAV messages")
plt.xticks(x, segment_labels)
plt.xlabel("Processed segment length (s)")
plt.ylabel("Count")
plt.title("GNSS-SDR validation after LCMV processing")
plt.legend()
plt.tight_layout()
fig2 = FIGS / "test_110_gnss_sdr_validation_metrics.png"
plt.savefig(fig2, dpi=200)
plt.close()

# Figure 3: before/after spectrum around injected jammer for 180 s case
FS = 2_400_000
JAM_HZ = 1500.0
N = 2**22

before_path = Path("/media/patryk/X31/jamguard_processed_test110/test_110_synth_jam_180s/ch0.cfile")
after_path = Path("/media/patryk/X31/jamguard_processed_test110/test_110_lcmv_180s/lcmv_ch0ref_null.cfile")
fig3 = FIGS / "test_110_180s_before_after_spectrum.png"

def spectrum_db(path, n, fs):
    x = np.fromfile(path, dtype=np.complex64, count=n)
    win = np.hanning(len(x))
    X = np.fft.fftshift(np.fft.fft(x * win))
    f = np.fft.fftshift(np.fft.fftfreq(len(x), d=1/fs))
    p = 20 * np.log10(np.abs(X) / np.sqrt(np.sum(win**2)) + 1e-12)
    return f, p

if before_path.exists() and after_path.exists():
    fb, pb = spectrum_db(before_path, N, FS)
    fa, pa = spectrum_db(after_path, N, FS)

    mask_b = np.abs(fb) <= 10_000
    mask_a = np.abs(fa) <= 10_000
    step_b = max(1, mask_b.sum() // 50_000)
    step_a = max(1, mask_a.sum() // 50_000)

    plt.figure(figsize=(9, 5))
    plt.plot(fb[mask_b][::step_b] / 1000, pb[mask_b][::step_b], label="Before nulling: synthetic jammed CH0")
    plt.plot(fa[mask_a][::step_a] / 1000, pa[mask_a][::step_a], label="After nulling: LCMV output")
    plt.axvline(JAM_HZ / 1000, linestyle="--", label="Injected jammer offset")
    plt.xlabel("Baseband frequency (kHz)")
    plt.ylabel("Magnitude (dB, relative)")
    plt.title("test_110 180 s before/after spectrum near injected jammer")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig3, dpi=200)
    plt.close()
else:
    print("Spectrum figure skipped because one of the 180 s files was missing.")

print("Wrote:")
print(csv_path)
print(md_path)
print(fig1)
print(fig2)
if fig3.exists():
    print(fig3)
