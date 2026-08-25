#!/usr/bin/env python3
"""BB84 quantum key distribution using PennyLane circuits."""

from __future__ import annotations

import random
import pennylane as qml
import numpy as np

NUM_BITS = 16
dev = qml.device("default.qubit", wires=1, shots=1)


@qml.qnode(dev)
def bb84_circuit(bit: int, encode_basis: str, measure_basis: str) -> int:
    if bit == 1:
        qml.PauliX(wires=0)
    if encode_basis == "+":
        qml.Hadamard(wires=0)
    if measure_basis == "+":
        qml.Hadamard(wires=0)
    return qml.sample(wires=0)


def run_bb84(eavesdrop: bool = False) -> None:
    print("=== BB84 Quantum Key Distribution (PennyLane) ===\n")

    alice_bits = [random.randint(0, 1) for _ in range(NUM_BITS)]
    alice_bases = [random.choice(["z", "+"]) for _ in range(NUM_BITS)]
    bob_bases = [random.choice(["z", "+"]) for _ in range(NUM_BITS)]

    print(f"  Alice bases: {' '.join(alice_bases)}")
    print(f"  Bob bases:   {' '.join(bob_bases)}\n")

    key_alice: list[int] = []
    key_bob: list[int] = []

    for i in range(NUM_BITS):
        if eavesdrop and random.random() < 0.5:
            eve_basis = random.choice(["z", "+"])
            _ = bb84_circuit(alice_bits[i], alice_bases[i], eve_basis)

        result = int(bb84_circuit(alice_bits[i], alice_bases[i], bob_bases[i]))
        key_bob.append(result)

        if alice_bases[i] == bob_bases[i]:
            key_alice.append(alice_bits[i])

    sift_a = [alice_bits[i] for i in range(NUM_BITS) if alice_bases[i] == bob_bases[i]]
    sift_b = [key_bob[i] for i in range(NUM_BITS) if alice_bases[i] == bob_bases[i]]

    print(f"  Sifted key (Alice): {sift_a}")
    print(f"  Sifted key (Bob):   {sift_b}")

    check = random.sample(range(len(sift_a)), min(4, len(sift_a)))
    errors = sum(1 for i in check if sift_a[i] != sift_b[i])
    qber = errors / len(check) if check else 0.0
    print(f"\n  QBER: {errors}/{len(check)} = {qber:.2%}")

    if qber > 0.11:
        print("  EAVESDROPPING DETECTED!")
    else:
        final = [sift_a[i] for i in range(len(sift_a)) if i not in check]
        print(f"  Final key ({len(final)} bits): {final}")


def main() -> None:
    print("=== No eavesdropper ===")
    run_bb84(eavesdrop=False)
    print("\n=== With eavesdropper ===")
    run_bb84(eavesdrop=True)


if __name__ == "__main__":
    main()
