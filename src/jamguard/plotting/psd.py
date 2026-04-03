"""PSD/FFT plotting functions."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_psd(iq: np.ndarray, sample_rate_hz: float, output_path: Path | None = None) -> None:
    """Plot simple FFT-based PSD for one channel."""
    fft = np.fft.fftshift(np.fft.fft(iq))
    freqs = np.fft.fftshift(np.fft.fftfreq(len(iq), d=1.0 / sample_rate_hz))
    psd = 20.0 * np.log10(np.abs(fft) + 1e-12)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(freqs, psd)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title("PSD")
    ax.grid(True)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
