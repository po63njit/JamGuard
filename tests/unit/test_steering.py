import numpy as np

from jamguard.geometry.uca import steering_matrix_azimuths, steering_vector_azimuth, uca_positions


def test_steering_vector_dimensions() -> None:
    pos = uca_positions(5, 0.076)
    v = steering_vector_azimuth(pos, 1_575_420_000.0, azimuth_deg=30.0)
    assert v.shape == (5,)
    assert np.iscomplexobj(v)


def test_steering_matrix_dimensions() -> None:
    pos = uca_positions(5, 0.076)
    m = steering_matrix_azimuths(pos, 1_575_420_000.0, np.array([-30.0, 0.0, 30.0]))
    assert m.shape == (3, 5)
