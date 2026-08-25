#!/usr/bin/env python3
"""Quantum Phase Estimation: estimate the eigenphase of a unitary.

QPE uses controlled powers of a unitary U to kick back eigenphases onto
precision qubits, then applies the inverse QFT to read the phase.

This demo estimates the eigenphase of the T gate (eigenvalue e^{i pi/4})
using 3 precision qubits. With 3 bits of precision the estimate should
be close to 1/8 = 0.125 of a full turn (= pi/4 radians).
"""

from __future__ import annotations

import math

import qiskit as qk
import qiskit_aer as qka


def qft_circuit(n: int) -> qk.QuantumCircuit:
    """Hand-rolled QFT on n qubits (Qiskit little-endian)."""
    qc = qk.QuantumCircuit(n, name="QFT")
    for j in range(n):
        qc.h(j)
        for k in range(j):
            qc.cp(math.pi / 2 ** (j - k), k, j)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    return qc


def inverse_qft_circuit(n: int) -> qk.QuantumCircuit:
    """Hand-rolled inverse QFT on n qubits."""
    qc = qk.QuantumCircuit(n, name="IQFT")
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    for j in range(n - 1, -1, -1):
        for k in range(j - 1, -1, -1):
            qc.cp(-math.pi / 2 ** (j - k), k, j)
        qc.h(j)
    return qc


def qpe_circuit(n_precision: int, eigenphase_bits: str) -> qk.QuantumCircuit:
    """QPE circuit: estimate the phase of the T gate (phase = 1/8).

    n_precision: number of precision qubits.
    eigenstate: the eigenstate |1> of T gate (T|1> = e^{i pi/4} |1>).

    Layout:
      q0..q_{n-1}: precision qubits (start in |+>^n, end with phase bits)
      q_n: eigenstate qubit (starts in |1>, holds the eigenstate)
    """
    n = n_precision + 1
    qc = qk.QuantumCircuit(n, n_precision, name="QPE")

    # prepare eigenstate |1> on the last qubit
    qc.x(n_precision)

    # put precision qubits in |+>^n
    qc.h(range(n_precision))

    # controlled powers of T gate
    for j in range(n_precision):
        for _ in range(2**j):
            qc.cp(math.pi / 4, j, n_precision)

    # inverse QFT on precision qubits
    qc.compose(inverse_qft_circuit(n_precision), inplace=True)

    # measure precision qubits
    qc.measure(range(n_precision), range(n_precision))
    return qc


def qpe_statevector(n_precision: int) -> None:
    """Show QPE result without measurement (statevector)."""
    n = n_precision + 1
    qc = qk.QuantumCircuit(n)
    qc.x(n_precision)
    qc.h(range(n_precision))

    for j in range(n_precision):
        for _ in range(2**j):
            qc.cp(math.pi / 4, j, n_precision)

    qc.compose(inverse_qft_circuit(n_precision), inplace=True)

    sv = qk.quantum_info.Statevector.from_instruction(qc)
    probs = sv.probabilities_dict()
    print(f"  {n_precision} precision qubits, statevector probabilities:")
    for state in sorted(probs.keys()):
        k = int(state[::-1], 2)
        phase_est = k / (2**n_precision)
        print(f"    |{state}>  k={k:2d}  phase estimate = {phase_est:.4f}  "
              f"(= {phase_est * 2 * math.pi:.4f} rad)  p = {probs[state]:.4f}")


def main() -> None:
    print("=== Quantum Phase Estimation ===\n")
    print("Target: T gate, eigenphase = 1/8 (= pi/4 rad)\n")

    for n_prec in (2, 3, 4):
        print(f"--- {n_prec} precision qubits ---")
        qpe_statevector(n_prec)
        print()

    n_prec = 3
    print(f"--- sampling QPE with {n_prec} precision qubits ---\n")
    qc = qpe_circuit(n_prec, "")
    print(qc.draw(output="text"))

    backend = qka.AerSimulator()
    counts = backend.run(qk.transpile(qc, backend), shots=4096).result().get_counts()
    print(f"\nshot histogram (top 5):")
    for bits, cnt in sorted(counts.items(), key=lambda kv: -kv[1])[:5]:
        k = int(bits, 2)
        phase_est = k / (2**n_prec)
        print(f"  |{bits}>  k={k}  phase = {phase_est:.4f}  ({cnt:4d} shots)")

    print("\nexact eigenphase = 0.125 (1/8)")
    print("\n=== done ===")


if __name__ == "__main__":
    main()
