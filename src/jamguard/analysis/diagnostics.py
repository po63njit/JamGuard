"""Channel health analysis utilities."""

from __future__ import annotations

import numpy as np

from jamguard.data.models import ChannelMetrics, MultiChannelCapture


def compute_channel_metrics(capture: MultiChannelCapture, preview_len: int = 1024) -> ChannelMetrics:
    """Compute per-channel mean power, RMS and preview snippets."""
    labels = capture.metadata.channel_labels
    mean_power: dict[str, float] = {}
    rms: dict[str, float] = {}
    preview: dict[str, list[float]] = {}

    for i, label in enumerate(labels):
        x = capture.data[i]
        p = float(np.mean(np.abs(x) ** 2))
        mean_power[label] = p
        rms[label] = float(np.sqrt(p))
        preview[label] = np.real(x[:preview_len]).astype(float).tolist()

    ranking = sorted(labels, key=lambda k: mean_power[k], reverse=True)
    return ChannelMetrics(mean_power=mean_power, rms=rms, ranking=ranking, preview=preview)


def metrics_table_text(metrics: ChannelMetrics) -> str:
    """Render a plain-text summary table."""
    lines = ["channel | mean_power | rms", "---|---:|---:"]
    for ch in metrics.ranking:
        lines.append(f"{ch} | {metrics.mean_power[ch]:.6e} | {metrics.rms[ch]:.6e}")
    return "\n".join(lines)
