"""Plotting helpers for MVP artifacts."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from jamguard.analysis.spectral import estimate_psd
from jamguard.beamforming.algorithms import beam_pattern_db
from jamguard.data.models import BeamformingResult, ChannelMetrics, MultiChannelCapture
from jamguard.geometry.uca import uca_positions


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_channel_power(metrics: ChannelMetrics, out_path: Path) -> None:
    labels = metrics.ranking
    vals = [metrics.mean_power[l] for l in labels]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(labels, vals)
    ax.set_title("Channel Mean Power")
    ax.set_ylabel("Power")
    ax.grid(True, axis="y", alpha=0.3)
    _save(fig, out_path)


def plot_channel_psd(capture: MultiChannelCapture, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, label in enumerate(capture.metadata.channel_labels):
        f, p = estimate_psd(capture.data[i], capture.metadata.sample_rate_hz)
        ax.plot(f / 1e6, p, label=label, alpha=0.8)
    ax.set_title("Per-channel PSD")
    ax.set_xlabel("Frequency offset (MHz)")
    ax.set_ylabel("PSD (dB/Hz)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _save(fig, out_path)


def plot_correlation_heatmap(matrix: np.ndarray, labels: list[str], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(matrix, vmin=0.0, vmax=1.0, cmap="viridis")
    ax.set_xticks(range(len(labels)), labels=labels)
    ax.set_yticks(range(len(labels)), labels=labels)
    ax.set_title("Correlation Magnitude Matrix")
    fig.colorbar(im, ax=ax)
    _save(fig, out_path)


def plot_phase_offsets(phases: dict[str, float], out_path: Path) -> None:
    labels = list(phases.keys())
    vals = [phases[l] for l in labels]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(labels, vals)
    ax.set_ylabel("Phase offset (rad)")
    ax.set_title("Relative Phase Offsets")
    ax.grid(True, axis="y", alpha=0.3)
    _save(fig, out_path)


def plot_beam_pattern(weights: np.ndarray, capture: MultiChannelCapture, out_path: Path) -> None:
    positions = uca_positions(capture.metadata.num_channels, capture.metadata.array_radius_m)
    az, resp_db = beam_pattern_db(weights, positions, capture.metadata.center_frequency_hz)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(az, resp_db)
    ax.set_ylim(-40, 1)
    ax.set_xlabel("Azimuth (deg)")
    ax.set_ylabel("Response (dB)")
    ax.set_title("Beam Pattern")
    ax.grid(True, alpha=0.3)
    _save(fig, out_path)


def plot_before_after_psd(
    capture: MultiChannelCapture,
    beam: BeamformingResult,
    out_path: Path,
) -> None:
    f0, p0 = estimate_psd(capture.data[0], capture.metadata.sample_rate_hz)
    fb, pb = estimate_psd(beam.output, capture.metadata.sample_rate_hz)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(f0 / 1e6, p0, label=f"{capture.metadata.channel_labels[0]} (input)")
    ax.plot(fb / 1e6, pb, label="beamformed", linewidth=2)
    ax.set_title("Before/After Beamforming PSD")
    ax.set_xlabel("Frequency offset (MHz)")
    ax.set_ylabel("PSD (dB/Hz)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _save(fig, out_path)
