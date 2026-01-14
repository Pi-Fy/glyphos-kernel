import random
import statistics

from glyphos_kernel.core import F_432, F_838_776, gate_11, gate_44
from glyphos_kernel.validation import build_retarded_mjlog, sample_minors, mean_resultant_length, phase_scramble

def main():
    rng = random.Random(0)
    X = [[rng.random(), rng.random()] for _ in range(24)]
    nu_i = [F_432, F_838_776] + [F_432 + i for i in range(2, 24)]
    a_j = [1.0, 1.618, 2.0, 2.618, 3.236]
    nu0 = F_432
    x_star = [0.5, 0.5]
    v = 1.0

    print(gate_11(nu_i, a_j, nu0))
    print(gate_44(nu_i, a_j, nu0))

    M, theta, tau = build_retarded_mjlog(X, nu_i, a_j, nu0, x_star, v, t=0.0)
    mags, phases = sample_minors(M, n_samples=20000, rng=rng)
    R = mean_resultant_length(phases)
    q = [statistics.quantiles(mags, n=100)[p-1] for p in (50, 90, 95, 99)]
    print(f"Minor stats: R={R:.4f}  q50={q[0]:.4g} q90={q[1]:.4g} q95={q[2]:.4g} q99={q[3]:.4g}")

    M_scr = phase_scramble(M, rng=rng)
    _, phases2 = sample_minors(M_scr, n_samples=20000, rng=rng)
    R2 = mean_resultant_length(phases2)
    print(f"Phase scramble control: R={R2:.4f}")

if __name__ == "__main__":
    main()
