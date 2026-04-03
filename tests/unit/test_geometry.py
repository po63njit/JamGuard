from jamguard.geometry.uca import uca_positions, wavelength_m


def test_uca_positions_shape() -> None:
    pos = uca_positions(num_elements=5, radius_m=0.076)
    assert pos.shape == (5, 3)


def test_wavelength_positive() -> None:
    wl = wavelength_m(1_575_420_000.0)
    assert wl > 0
