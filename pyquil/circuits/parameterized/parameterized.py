from pyquil import Program, get_qc
from pyquil.gates import RZ, MEASURE
import numpy as np


def parameterized_circuit(theta_values):
    p = Program()
    ro = p.declare("ro", "BIT", 1)
    theta = p.declare("theta", "REAL")

    p += RZ(theta, 0)
    p += MEASURE(0, ro[0])

    qc = get_qc("1q-qvm")

    results = []
    for val in theta_values:
        bitstrings = qc.run(qc.compile(p), memory_map={"theta": [val]})
        results.append((val, bitstrings.readout_data.get("ro")))
    return results


def main():
    thetas = [0.0, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]
    results = parameterized_circuit(thetas)
    for theta, ro in results:
        print(f"theta={theta:.4f} -> {ro}")


if __name__ == "__main__":
    main()
