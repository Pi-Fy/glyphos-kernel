import random
from glyphos_kernel.validation import build_retarded_mjlog, sample_minors, mean_resultant_length, phase_scramble, tau_shuffle
from glyphos_kernel.phase import retarded_phase_matrix

def test_validation_smoke():
    rng = random.Random(0)
    X = [[rng.random(), rng.random()] for _ in range(12)]
    nu_i = [432.0 + i for i in range(12)]
    a_j = [1.0, 1.618, 2.0, 2.618]
    nu0 = 432.0
    x_star = [0.5, 0.5]
    v = 1.0

    M, theta, tau = build_retarded_mjlog(X, nu_i, a_j, nu0, x_star, v, t=0.0)

    mags, phases = sample_minors(M, n_samples=3000, rng=rng)
    R = mean_resultant_length(phases)
    assert 0.0 <= R <= 1.0
    assert len(mags) == 3000

    M_scr = phase_scramble(M, rng=rng)
    _, phases2 = sample_minors(M_scr, n_samples=1500, rng=rng)
    R2 = mean_resultant_length(phases2)
    assert 0.0 <= R2 <= 1.0

    tau2 = tau_shuffle(tau, rng=rng)
    theta2 = retarded_phase_matrix(a_j=a_j, tau_i=tau2, nu0_hz=nu0, t=0.0)
    assert len(theta2) == len(theta)
