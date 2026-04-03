"""Time-domain plotting helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_iq_timeseries(iq: np.ndarray, output_path: Path | None = None, max_samples: int = 5000) -> None:
    """Plot real/imaginary time traces of one IQ stream."""
    y = iq[:max_samples]
    x = np.arange(len(y))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y.real, label="I")
    ax.plot(x, y.imag, label="Q")
    ax.legend()
    ax.set_title("Time Domain IQ")
    ax.grid(True)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
