#!/usr/bin/env python3
"""Quantum random number generation.

Measure Hadamard-created superpositions to extract truly random bits.
Runs statistical tests (chi-squared) to verify randomness.
"""

from __future__ import annotations

import math

import qiskit as qk
import qiskit_aer as qka

NUM_BITS = 100
NUM_SAMPLES = 1000


def quantum_random_bit() -> int:
    qc = qk.QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    backend = qka.AerSimulator()
    compiled = qk.transpile(qc, backend)
    counts = backend.run(compiled, shots=1).result().get_counts()
    return int(list(counts.keys())[0], 2)


def generate_random_bits(n: int) -> list[int]:
    qc = qk.QuantumCircuit(n, n)
    for i in range(n):
        qc.h(i)
    qc.measure(range(n), range(n))
    backend = qka.AerSimulator()
    compiled = qk.transpile(qc, backend)
    counts = backend.run(compiled, shots=1).result().get_counts()
    bitstring = list(counts.keys())[0]
    return [int(b) for b in bitstring.zfill(n)]


def chi_squared_test(bits: list[int]) -> float:
    n = len(bits)
    ones = sum(bits)
    zeros = n - ones
    expected = n / 2
    chi2 = ((zeros - expected) ** 2 + (ones - expected) ** 2) / expected
    return chi2


def frequency_in_byte(bits: list[int]) -> dict[str, int]:
    freq: dict[str, int] = {}
    for i in range(0, len(bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val = (byte_val << 1) | bits[i + j]
        key = f"{byte_val:03d}"
        freq[key] = freq.get(key, 0) + 1
    return freq


def main() -> None:
    print("=== Quantum Random Number Generator ===\n")

    print("Single random bits:")
    single_bits = [quantum_random_bit() for _ in range(16)]
    print(f"  {''.join(map(str, single_bits))}")

    print(f"\nGenerating {NUM_BITS} random bits:")
    bits = generate_random_bits(NUM_BITS)
    bitstring = "".join(map(str, bits))
    print(f"  {bitstring[:64]}...")
    print(f"  ({len(bitstring)} bits total)")

    ones = sum(bits)
    zeros = len(bits) - ones
    print(f"\nFrequency: 0s={zeros}, 1s={ones}")

    chi2 = chi_squared_test(bits)
    print(f"Chi-squared: {chi2:.4f} (critical value at p=0.05: 3.841)")
    print(f"  {'PASS — distribution is uniform' if chi2 < 3.841 else 'FAIL — distribution is biased'}")

    print(f"\nGenerating {NUM_SAMPLES} random bits for byte frequency analysis:")
    sample_bits = generate_random_bits(NUM_SAMPLES)
    freq = frequency_in_byte(sample_bits)
    print(f"  Unique byte values seen: {len(freq)}/128")
    print(f"  Chi-squared uniformity: ", end="")
    total_bytes = sum(freq.values())
    expected = total_bytes / 128
    chi2_byte = sum((v - expected) ** 2 / expected for v in freq.values())
    print(f"{chi2_byte:.2f}")
    print(f"  {'PASS — bytes are uniformly distributed' if chi2_byte < 200 else 'FAIL — byte distribution is biased'}")

    print("\nQuantum RNG advantage: measurement outcomes are")
    print("inherently unpredictable — no classical algorithm can")
    print("reproduce them without the quantum state.")


if __name__ == "__main__":
    main()
