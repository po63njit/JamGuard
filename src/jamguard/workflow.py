from __future__ import annotations
from pathlib import Path
import json
import csv
import numpy as np
from .io.cfile import load_multichannel_capture, write_complex64_cfile, cfile_sample_count
from .dsp.metrics import summarize_channel
from .dsp.coherence import normalized_xcorr_lag, windowed_lag_analysis
from .dsp.calibration import estimate_all_phase_corrections, apply_phase_corrections
from .dsp.jammer import generate_tone_jammer, inject_spatial_interferer
from .dsp.beamforming import covariance_matrix, lcmv_weights, apply_weights


def _channel_paths(input_dir: Path, channels: int, pattern: str) -> list[Path]:
    return [input_dir / pattern.format(ch) for ch in range(channels)]


def check_capture_files(input_dir: str | Path, channels: int = 5, pattern: str = "ch{}.cfile") -> list[dict]:
    root = Path(input_dir)
    rows = []
    for ch, fp in enumerate(_channel_paths(root, channels, pattern)):
        if not fp.exists():
            raise FileNotFoundError(f"missing channel file: {fp}")
        rows.append({"channel": ch, "path": str(fp), "samples": cfile_sample_count(fp), "bytes": fp.stat().st_size})
    return rows


def channel_health(input_dir: str | Path, sample_rate: float, channels: int = 5, pattern: str = "ch{}.cfile", max_samples: int | None = None) -> list[dict]:
    X = load_multichannel_capture(input_dir, pattern=pattern, channels=channels, count=max_samples)
    return [{"channel": ch, **summarize_channel(X[ch], sample_rate)} for ch in range(channels)]


def coarse_lag(input_dir: str | Path, sample_rate: float, channels: int = 5, pattern: str = "ch{}.cfile", max_samples: int | None = None) -> list[dict]:
    X = load_multichannel_capture(input_dir, pattern=pattern, channels=channels, count=max_samples)
    out = []
    for ch in range(1, channels):
        lag, corr = normalized_xcorr_lag(X[0], X[ch], 64)
        out.append({"channel": ch, "lag_samples": lag, "lag_seconds": lag / sample_rate, "corr": corr})
    return out


def multi_window(input_dir: str | Path, sample_rate: float, channels: int = 5, pattern: str = "ch{}.cfile", max_samples: int | None = None, window_samples: int = 2048, hop_samples: int = 1024) -> list[dict]:
    X = load_multichannel_capture(input_dir, pattern=pattern, channels=channels, count=max_samples)
    return windowed_lag_analysis(X, sample_rate, window_samples=min(window_samples, X.shape[1]), hop_samples=max(1, min(hop_samples, X.shape[1])))


def phase_align(input_dir: str | Path, output_dir: str | Path, channels: int = 5, pattern: str = "ch{}.cfile", max_samples: int | None = None, force: bool = False) -> dict:
    out = Path(output_dir)
    if out.exists() and any(out.iterdir()) and not force:
        raise FileExistsError(f"output exists, use --force: {out}")
    X = load_multichannel_capture(input_dir, pattern=pattern, channels=channels, count=max_samples)
    corr = estimate_all_phase_corrections(X)
    Y = apply_phase_corrections(X, corr)
    out.mkdir(parents=True, exist_ok=True)
    for ch in range(channels):
        write_complex64_cfile(out / pattern.format(ch), Y[ch])
    manifest = {"corrections": [{"channel": i, "re": float(np.real(c)), "im": float(np.imag(c))} for i, c in enumerate(corr)]}
    (out / "phase_alignment.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def inject_jammer(input_dir: str | Path, output_dir: str | Path, sample_rate: float, channels: int = 5, pattern: str = "ch{}.cfile", max_samples: int | None = None, amplitude: float = 3.0, offset_hz: float = 1500.0, force: bool = False) -> dict:
    out = Path(output_dir)
    if out.exists() and any(out.iterdir()) and not force:
        raise FileExistsError(f"output exists, use --force: {out}")
    X = load_multichannel_capture(input_dir, pattern=pattern, channels=channels, count=max_samples)
    jammer = generate_tone_jammer(X.shape[1], sample_rate, offset_hz=offset_hz, amplitude=amplitude)
    sig = np.exp(1j * np.linspace(0, np.pi/2, channels)).astype(np.complex64)
    Y = inject_spatial_interferer(X, jammer, sig)
    out.mkdir(parents=True, exist_ok=True)
    for ch in range(channels):
        write_complex64_cfile(out / pattern.format(ch), Y[ch])
    manifest = {"sample_rate": sample_rate, "channels": channels, "amplitude": amplitude, "offset_hz": offset_hz, "signature_phase_rad": [float(np.angle(v)) for v in sig]}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def run_lcmv(input_dir: str | Path, output_dir: str | Path, metrics_csv: str | Path, sample_rate: float, channels: int = 5, pattern: str = "ch{}.cfile", max_samples: int | None = None, force: bool = False) -> dict:
    out = Path(output_dir)
    if out.exists() and any(out.iterdir()) and not force:
        raise FileExistsError(f"output exists, use --force: {out}")
    X = load_multichannel_capture(input_dir, pattern=pattern, channels=channels, count=max_samples)
    R = covariance_matrix(X, diagonal_loading=1e-3)
    c_look = np.ones(channels, dtype=np.complex64)
    c_null = np.exp(1j * np.linspace(0, np.pi/2, channels)).astype(np.complex64)
    C = np.column_stack([c_look, c_null])
    f = np.array([1+0j, 0+0j], dtype=np.complex64)
    w = lcmv_weights(R, C, f)
    y = apply_weights(X, w)
    out.mkdir(parents=True, exist_ok=True)
    write_complex64_cfile(out / "lcmv_ch0ref_null.cfile", y)
    metrics = {"samples": int(len(y)), "output_power_db": float(10*np.log10(np.mean(np.abs(y)**2)+1e-12)), "sample_rate": sample_rate}
    (out / "weights.json").write_text(json.dumps({"weights": [{"re": float(np.real(v)), "im": float(np.imag(v))} for v in w], "metrics": metrics}, indent=2))
    mpath = Path(metrics_csv); mpath.parent.mkdir(parents=True, exist_ok=True)
    with mpath.open("w", newline="") as fcsv:
        wcsv = csv.DictWriter(fcsv, fieldnames=list(metrics.keys()))
        wcsv.writeheader(); wcsv.writerow(metrics)
    return metrics
