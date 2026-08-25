from pyquil import Program, get_qc
from pyquil.gates import H, PHASE, MEASURE
import numpy as np


def phase_shift(theta: float) -> list:
    """Apply Hadamard then a phase shift and measure.

    Args:
        theta: Phase angle in radians.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 1)

    p += H(0)
    p += PHASE(theta, 0)
    p += H(0)
    p += MEASURE(0, ro[0])

    qc = get_qc("1q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main() -> None:
    thetas = [0.0, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2]
    for theta in thetas:
        results = phase_shift(theta)
        counts = {}
        for row in results:
            key = "".join(str(b) for b in row)
            counts[key] = counts.get(key, 0) + 1
        print(f"theta={theta:.4f} -> Counts: {counts}")


if __name__ == "__main__":
    main()
