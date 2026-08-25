#!/usr/bin/env python3
"""BB84 quantum key distribution protocol.

Alice encodes random bits in random bases, Bob measures in random bases.
They publicly compare bases, keep matching ones, then check a subset for
eavesdropping via quantum bit error rate (QBER).
"""

from __future__ import annotations

import random

import qiskit as qk
import qiskit_aer as qka

SHOTS = 1
NUM_BITS = 16
EAVESDROP = False


def encode_bit(bit: int, basis: str) -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == "+":
        qc.h(0)
    return qc


def measure_bit(qc: qk.QuantumCircuit, basis: str) -> int:
    if basis == "+":
        qc.h(0)
    qc.measure(0, 0)
    backend = qka.AerSimulator()
    compiled = qk.transpile(qc, backend)
    counts = backend.run(compiled, shots=1).result().get_counts()
    return int(list(counts.keys())[0], 2)


def run_bb84(eavesdrop: bool = False) -> None:
    alice_bits = [random.randint(0, 1) for _ in range(NUM_BITS)]
    alice_bases = [random.choice(["z", "+"]) for _ in range(NUM_BITS)]
    bob_bases = [random.choice(["z", "+"]) for _ in range(NUM_BITS)]

    print("=== BB84 Quantum Key Distribution ===\n")
    print(f"  bits:     {alice_bits}")
    print(f"  Alice's bases: {' '.join(alice_bases)}")
    print(f"  Bob's bases:   {' '.join(bob_bases)}\n")

    key_alice: list[int] = []
    key_bob: list[int] = []

    for i in range(NUM_BITS):
        qc = encode_bit(alice_bits[i], alice_bases[i])

        if eavesdrop and random.random() < 0.5:
            eve_basis = random.choice(["z", "+"])
            measure_bit(qc, eve_basis)

        result = measure_bit(qc, bob_bases[i])
        key_bob.append(result)

        if alice_bases[i] == bob_bases[i]:
            key_alice.append(alice_bits[i])

    print(f"  Alice's raw key (matching bases): {key_alice}")
    print(f"  Bob's raw key (matching bases):   {key_bob}")

    sift_alice: list[int] = []
    sift_bob: list[int] = []
    for i in range(NUM_BITS):
        if alice_bases[i] == bob_bases[i]:
            sift_alice.append(alice_bits[i])
            sift_bob.append(key_bob[i])

    print(f"\n  Sifted key (Alice): {sift_alice}")
    print(f"  Sifted key (Bob):   {sift_bob}")

    check_bits = min(4, len(sift_alice))
    check_indices = random.sample(range(len(sift_alice)), check_bits)
    errors = sum(1 for i in check_indices if sift_alice[i] != sift_bob[i])
    qber = errors / check_bits if check_bits > 0 else 0.0

    print(f"\n  Check bits indices: {check_indices}")
    print(f"  Errors: {errors}/{check_bits}  QBER = {qber:.2%}")

    if qber > 0.11:
        print("  *** EAVESDROPPING DETECTED *** (QBER > 11%)")
        print("  Key is insecure — abort!")
    else:
        remaining = [sift_alice[i] for i in range(len(sift_alice)) if i not in check_indices]
        print(f"\n  Final key ({len(remaining)} bits): {remaining}")
        print("  QBER acceptable — key is secure.")


def main() -> None:
    print("=== No eavesdropper ===\n")
    run_bb84(eavesdrop=False)
    print("\n\n=== With eavesdropper ===\n")
    run_bb84(eavesdrop=True)


if __name__ == "__main__":
    main()
