import math
from glyphos_kernel.core import golden_pi, bridge_frequency, harmonic_ladder, F_432, PHI, PI

def test_golden_pi_value():
    pi_phi = golden_pi(PHI)
    assert math.isfinite(pi_phi)
    assert pi_phi > 0

def test_bridge_frequency_locked():
    fb = bridge_frequency(F_432, PI, PHI)
    assert math.isfinite(fb)
    assert fb > 0

def test_harmonic_ladder_monotone_in_n():
    f0 = 432.0
    f1 = harmonic_ladder(f0, 1, 0)
    f2 = harmonic_ladder(f0, 2, 0)
    assert f2 > f1 > 0
