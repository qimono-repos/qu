#!/usr/bin/env python3
"""E91 entanglement-based QKD using PennyLane."""

from __future__ import annotations

import random
import pennylane as qml
import numpy as np

NUM_PAIRS = 20
dev = qml.device("default.qubit", wires=2, shots=1)


@qml.qnode(dev)
def e91_measure(alice_basis: int, bob_basis: int) -> tuple[int, int]:
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])

    if alice_basis == 1:
        qml.RY(3 * np.pi / 4, wires=0)
    elif alice_basis == 2:
        qml.RY(np.pi / 4, wires=0)

    if bob_basis == 1:
        qml.RY(3 * np.pi / 4, wires=1)
    elif bob_basis == 2:
        qml.RY(np.pi / 4, wires=1)

    return qml.sample(wires=[0, 1])


def run_e91() -> None:
    print("=== E91 Entanglement-Based QKD (PennyLane) ===\n")

    alice_bases = [random.choice([0, 1, 2]) for _ in range(NUM_PAIRS)]
    bob_bases = [random.choice([0, 1, 2]) for _ in range(NUM_PAIRS)]

    alice_results: list[int] = []
    bob_results: list[int] = []

    for i in range(NUM_PAIRS):
        sample = e91_measure(alice_bases[i], bob_bases[i])
        alice_results.append(int(sample[0]))
        bob_results.append(int(sample[1]))

    matching = [
        (i, alice_bases[i], alice_results[i], bob_results[i])
        for i in range(NUM_PAIRS)
        if alice_bases[i] == bob_bases[i]
    ]

    print(f"Matching basis pairs: {len(matching)}/{NUM_PAIRS}")
    for idx, basis, a_val, b_val in matching:
        print(f"  pair {idx:2d}  basis={basis}  A={a_val}  B={b_val}  {'match' if a_val == b_val else 'MISMATCH'}")

    key_a = [a for _, _, a, _ in matching]
    key_b = [b for _, _, _, b in matching]

    print(f"\nRaw key (Alice): {key_a}")
    print(f"Raw key (Bob):   {key_b}")

    check_count = max(1, int(len(key_a) * 0.25))
    check_indices = random.sample(range(len(key_a)), min(check_count, len(key_a)))
    errors = sum(1 for i in check_indices if key_a[i] != key_b[i])
    qber = errors / len(check_indices) if check_indices else 0.0

    print(f"\nQBER: {errors}/{len(check_indices)} = {qber:.2%}")
    if qber > 0.11:
        print("Eavesdropping detected!")
    else:
        final = [key_a[i] for i in range(len(key_a)) if i not in check_indices]
        print(f"Secure key ({len(final)} bits): {final}")


def main() -> None:
    run_e91()


if __name__ == "__main__":
    main()
