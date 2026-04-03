"""Legacy PSD plotting wrappers."""

from __future__ import annotations

from pathlib import Path

from jamguard.analysis.spectral import estimate_psd


def plot_psd(iq, sample_rate_hz: float, output_path: Path | None = None) -> None:
    """Backward-compatible placeholder for single-channel PSD generation."""
    import matplotlib.pyplot as plt

    f, p = estimate_psd(iq, sample_rate_hz)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(f, p)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("PSD (dB/Hz)")
    ax.grid(True)
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
