"""Equal-superposition stats for n qubits: H^⊗n |0...0>.

Usage:
    uv run superposition-stats 4
"""
import argparse
import math

import numpy as np

H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # single-qubit Hadamard


def superposition_stats(n: int) -> tuple[int, float, float]:
    """Return (summands, amplitude, probability per outcome) for H^⊗n |0...0>."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be an integer >= 1")
    U = H
    for _ in range(n - 1):
        U = np.kron(U, H)          # H ⊗ H ⊗ ... (n times)
    psi = U[:, 0]                  # H^⊗n |0...0> = first column of U
    if not np.allclose(psi, psi[0]):
        raise ArithmeticError("amplitudes are not all equal")
    if not math.isclose(float(np.sum(np.abs(psi) ** 2)), 1.0):
        raise ArithmeticError("state is not normalized")
    amplitude = float(psi[0])
    return len(psi), amplitude, amplitude ** 2


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="superposition-stats",
        description="Equal-superposition stats for n qubits (H on each qubit from |0...0>)",
    )
    parser.add_argument("n", type=int, help="number of qubits")
    n = parser.parse_args().n
    summands, amp, prob = superposition_stats(n)
    print(f"n={n}: summands={summands}, amplitude={amp:.6f}, P per outcome={prob:.6f}")


if __name__ == "__main__":
    main()
