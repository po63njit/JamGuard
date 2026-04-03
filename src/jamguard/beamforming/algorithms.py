"""Fixed beamforming algorithms for JamGuard MVP."""

from __future__ import annotations

import numpy as np

from jamguard.data.models import BeamformingResult, MultiChannelCapture
from jamguard.geometry.uca import steering_vector_azimuth, uca_positions


def delay_and_sum_beamform(capture: MultiChannelCapture, azimuth_deg: float) -> BeamformingResult:
    """Conventional beamforming steered to azimuth."""
    md = capture.metadata
    positions = uca_positions(md.num_channels, md.array_radius_m)
    steering = steering_vector_azimuth(positions, md.center_frequency_hz, azimuth_deg)
    weights = steering / md.num_channels

    y = weights.conj() @ capture.data
    input_p = float(np.mean(np.abs(capture.data) ** 2))
    output_p = float(np.mean(np.abs(y) ** 2))
    return BeamformingResult(
        azimuth_deg=azimuth_deg,
        weights=weights,
        output=y.astype(np.complex64),
        input_mean_power=input_p,
        output_mean_power=output_p,
    )


def beam_pattern_db(weights: np.ndarray, positions_m: np.ndarray, center_frequency_hz: float) -> tuple[np.ndarray, np.ndarray]:
    """Compute normalized array response over azimuth angles."""
    az = np.linspace(-180.0, 180.0, 361)
    resp = []
    for a in az:
        sv = steering_vector_azimuth(positions_m, center_frequency_hz, float(a))
        resp.append(np.abs(weights.conj() @ sv))
    resp_arr = np.asarray(resp)
    resp_db = 20 * np.log10(resp_arr / (np.max(resp_arr) + 1e-12) + 1e-12)
    return az, resp_db
