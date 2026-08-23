#!/usr/bin/env python3
"""Grover search over 3 qubits, built from an oracle and a diffuser.

The marked item is the computational-basis state |101>. With N = 8
addresses and one solution the optimal iteration count is
floor(pi/4 * sqrt(N)) = 2. Oracle, diffuser, and driver all live in
this file; nothing is imported from the other algorithm folders.
"""

from __future__ import annotations

import math

import qiskit as qk
from qiskit_aer import AerSimulator


N_QUBITS = 3
MARKED = "101"


def phase_oracle(marked: str) -> qk.QuantumCircuit:
    """Phase-flip the single marked computational-basis state."""
    if len(marked) != N_QUBITS or any(ch not in "01" for ch in marked):
        raise ValueError(f"marked state must be a {N_QUBITS}-bit string")
    oracle = qk.QuantumCircuit(N_QUBITS, name="oracle")
    # Qiskit qubit 0 is the rightmost character of the bitstring.
    zeros = [i for i, bit in enumerate(reversed(marked)) if bit == "0"]
    for q in zeros:
        oracle.x(q)
    oracle.h(N_QUBITS - 1)
    oracle.mcx(list(range(N_QUBITS - 1)), N_QUBITS - 1)
    oracle.h(N_QUBITS - 1)
    for q in zeros:
        oracle.x(q)
    return oracle


def diffuser(n: int) -> qk.QuantumCircuit:
    """Reflection about the uniform superposition: 2|s><s| - I."""
    diff = qk.QuantumCircuit(n, name="diffuser")
    diff.h(range(n))
    diff.x(range(n))
    diff.h(n - 1)
    diff.mcx(list(range(n - 1)), n - 1)
    diff.h(n - 1)
    diff.x(range(n))
    diff.h(range(n))
    return diff


def grover_circuit(marked: str, iterations: int) -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(N_QUBITS, N_QUBITS, name="grover")
    qc.h(range(N_QUBITS))
    oracle = phase_oracle(marked)
    spread = diffuser(N_QUBITS)
    for _ in range(iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(spread, inplace=True)
    qc.measure(range(N_QUBITS), range(N_QUBITS))
    return qc


def success_probability(marked: str, iterations: int) -> float:
    qc = qk.QuantumCircuit(N_QUBITS)
    qc.h(range(N_QUBITS))
    oracle = phase_oracle(marked)
    spread = diffuser(N_QUBITS)
    for _ in range(iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(spread, inplace=True)
    probs = qk.quantum_info.Statevector.from_instruction(qc).probabilities_dict()
    return float(probs.get(marked, 0.0))


def main() -> None:
    n_items = 2**N_QUBITS
    optimal = int(math.floor(math.pi / 4 * math.sqrt(n_items)))
    print(f"Grover search, {n_items} items, marked state |{MARKED}>")
    print(f"optimal iterations ≈ π/4 √N = {optimal}\n")

    print("amplitude on the marked state after k Grover iterates:")
    for k in range(0, optimal + 3):
        p = success_probability(MARKED, k)
        bar = "#" * int(round(40 * p))
        print(f"  k={k}: p={p:6.3f}  {bar}")

    qc = grover_circuit(MARKED, optimal)
    print("\nfull circuit")
    print(qc.draw(output="text"))

    backend = AerSimulator()
    counts = backend.run(qk.transpile(qc, backend), shots=2048).result().get_counts()
    print("\nshot histogram:")
    for bits, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        flag = "  <-- marked" if bits == MARKED else ""
        print(f"  |{bits}>  {n:4d}{flag}")


if __name__ == "__main__":
    main()
