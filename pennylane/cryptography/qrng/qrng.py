#!/usr/bin/env python3
"""Quantum random number generation using PennyLane."""

from __future__ import annotations

import pennylane as qml
import numpy as np

NUM_BITS = 1000
dev = qml.device("default.qubit", wires=1, shots=1)


@qml.qnode(dev)
def random_bit() -> int:
    qml.Hadamard(wires=0)
    return qml.sample(wires=0)


@qml.qnode(dev)
def random_bits(n: int) -> np.ndarray:
    for i in range(n):
        qml.Hadamard(wires=i)
    return qml.sample(wires=range(n))


def chi_squared_test(bits: list[int]) -> float:
    n = len(bits)
    ones = sum(bits)
    zeros = n - ones
    expected = n / 2
    return ((zeros - expected) ** 2 + (ones - expected) ** 2) / expected


def main() -> None:
    print("=== Quantum Random Number Generator (PennyLane) ===\n")

    print("16 single-shot random bits:")
    bits = [int(random_bit()) for _ in range(16)]
    print(f"  {''.join(map(str, bits))}")

    print(f"\nGenerating {NUM_BITS} random bits:")
    try:
        sample = random_bits(NUM_BITS)
        all_bits = [int(b) for b in sample]
    except Exception:
        all_bits = [int(random_bit()) for _ in range(NUM_BITS)]

    ones = sum(all_bits)
    zeros = len(all_bits) - ones
    print(f"  Frequency: 0s={zeros}, 1s={ones}")

    chi2 = chi_squared_test(all_bits)
    print(f"  Chi-squared: {chi2:.4f} (critical value 3.841 at p=0.05)")
    print(f"  {'PASS' if chi2 < 3.841 else 'FAIL'}")

    print("\nQuantum RNG: measurement outcomes are inherently")
    print("unpredictable — no classical algorithm can reproduce them.")


if __name__ == "__main__":
    main()
