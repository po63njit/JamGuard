from jamguard.geometry.uca import uca_positions


def test_uca_positions_shape() -> None:
    pos = uca_positions(num_elements=5, radius_m=0.076)
    assert pos.shape == (5, 3)
