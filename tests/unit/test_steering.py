import numpy as np

from jamguard.beamforming.steering import steering_vector
from jamguard.geometry.uca import uca_positions


def test_steering_vector_dimensions() -> None:
    pos = uca_positions(5, 0.076)
    v = steering_vector(pos, 1_575_420_000.0, az_deg=0.0, el_deg=0.0)
    assert v.shape == (5,)
    assert np.iscomplexobj(v)
