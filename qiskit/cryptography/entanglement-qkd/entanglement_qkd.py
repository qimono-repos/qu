#!/usr/bin/env python3
"""E91 entanglement-based quantum key distribution.

Alice and Bob share Bell pairs. Each measures in a randomly chosen basis.
After measurement they publicly compare bases, keep matching ones, and
verify security via CHSH-type correlations.
"""

from __future__ import annotations

import random

import qiskit as qk
import qiskit_aer as qka

NUM_PAIRS = 20
CHECK_FRACTION = 0.25

ALICE_bases = [0, 1, 2]
BOB_bases = [0, 1, 2]


def create_bell_pair() -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def alice_measure(qc: qk.QuantumCircuit, basis: int, shots: int = 1) -> int:
    if basis == 1:
        qc.ry(3 * 3.14159265 / 4, 0)
    elif basis == 2:
        qc.ry(3.14159265 / 4, 0)
    qc.measure(0, 0)
    backend = qka.AerSimulator()
    compiled = qk.transpile(qc, backend)
    counts = backend.run(compiled, shots=shots).result().get_counts()
    return int(list(counts.keys())[0], 2)


def bob_measure(qc: qk.QuantumCircuit, basis: int, shots: int = 1) -> int:
    if basis == 1:
        qc.ry(3 * 3.14159265 / 4, 1)
    elif basis == 2:
        qc.ry(3.14159265 / 4, 1)
    qc.measure(1, 1)
    backend = qka.AerSimulator()
    compiled = qk.transpile(qc, backend)
    counts = backend.run(compiled, shots=shots).result().get_counts()
    return int(list(counts.keys())[0], 2)


def run_e91() -> None:
    print("=== E91 Entanglement-Based QKD ===\n")

    alice_bases = [random.choice(ALICE_bases) for _ in range(NUM_PAIRS)]
    bob_bases = [random.choice(BOB_bases) for _ in range(NUM_PAIRS)]

    alice_results: list[int] = []
    bob_results: list[int] = []

    for i in range(NUM_PAIRS):
        qc = create_bell_pair()
        a = alice_measure(qc, alice_bases[i])
        b = bob_measure(qc, bob_bases[i])
        alice_results.append(a)
        bob_results.append(b)

    print(f"Alice bases: {alice_bases}")
    print(f"Bob bases:   {bob_bases}")
    print(f"Alice results: {alice_results}")
    print(f"Bob results:   {bob_results}\n")

    matching: list[tuple[int, int, int, int]] = []
    for i in range(NUM_PAIRS):
        if alice_bases[i] == bob_bases[i]:
            matching.append((i, alice_bases[i], alice_results[i], bob_results[i]))

    print(f"Matching basis pairs: {len(matching)}/{NUM_PAIRS}")
    for idx, basis, a_val, b_val in matching:
        print(f"  pair {idx:2d}  basis={basis}  A={a_val}  B={b_val}  {'match' if a_val == b_val else 'MISMATCH'}")

    key_alice = [a for _, _, a, _ in matching]
    key_bob = [b for _, _, _, b in matching]

    print(f"\nRaw key (Alice): {key_alice}")
    print(f"Raw key (Bob):   {key_bob}")

    check_count = max(1, int(len(key_alice) * CHECK_FRACTION))
    check_indices = random.sample(range(len(key_alice)), min(check_count, len(key_alice)))
    errors = sum(1 for i in check_indices if key_alice[i] != key_bob[i])
    qber = errors / len(check_indices) if check_indices else 0.0

    print(f"\nQBER: {errors}/{len(check_indices)} = {qber:.2%}")
    if qber > 0.11:
        print("Eavesdropping detected! Aborting key exchange.")
    else:
        final_key = [key_alice[i] for i in range(len(key_alice)) if i not in check_indices]
        print(f"Secure key ({len(final_key)} bits): {final_key}")

    print("\nCHSH correlation check (basis 0,0):")
    s00 = [(a, b) for i, (ab, bb, a, b) in enumerate(matching) if ab == 0 and bb == 0]
    if s00:
        agree = sum(1 for a, b in s00 if a == b)
        print(f"  P(A==B) = {agree}/{len(s00)} = {agree / len(s00):.2f}")
        print("  For Bell |Phi+>: P(A==B) ~ 1.0 (perfect correlation)")


def main() -> None:
    run_e91()


if __name__ == "__main__":
    main()
