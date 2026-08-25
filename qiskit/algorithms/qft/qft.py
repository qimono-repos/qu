#!/usr/bin/env python3
"""Quantum Fourier Transform on 3–4 qubits.

The QFT maps |j> to (1/sqrt(N)) sum_k e^{2pi i jk/N} |k>. It is the
quantum analogue of the discrete Fourier transform and is the key
subroutine in Shor's algorithm and quantum phase estimation.

This demo builds the QFT gate-by-gate, verifies it against the
classical DFT matrix, and shows the frequency decomposition of a
simple input state.
"""

from __future__ import annotations

import cmath
import math

import qiskit as qk
import qiskit_aer as qka


def qft_circuit(n: int) -> qk.QuantumCircuit:
    """Hand-rolled QFT on n qubits (Qiskit little-endian convention).

    In Qiskit's ordering, qubit 0 is the least-significant bit.
    The QFT applies H on qubit j, then controlled phase rotations
    from qubits 0..j-1 onto qubit j, then swaps to reverse the
    bit order.
    """
    qc = qk.QuantumCircuit(n, name=f"QFT-{n}")
    for j in range(n):
        qc.h(j)
        for k in range(j):
            qc.cp(math.pi / 2 ** (j - k), k, j)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    return qc


def inverse_qft_circuit(n: int) -> qk.QuantumCircuit:
    """Hand-rolled inverse QFT on n qubits."""
    qc = qk.QuantumCircuit(n, name=f"IQFT-{n}")
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    for j in range(n - 1, -1, -1):
        for k in range(j - 1, -1, -1):
            qc.cp(-math.pi / 2 ** (j - k), k, j)
        qc.h(j)
    return qc


def dft_matrix(n: int) -> list[list[complex]]:
    """Classical DFT matrix for reference."""
    N = 2**n
    return [
        [cmath.exp(2j * math.pi * j * k / N) / math.sqrt(N) for k in range(N)]
        for j in range(N)
    ]


def verify_qft(n: int) -> None:
    """Verify QFT by checking: QFT then IQFT returns the original state,
    and QFT(|+>^n) = |0>."""
    ok = True
    N = 2**n
    # test roundtrip on a few basis states
    for j in (0, 1, N // 2, N - 1):
        qc = qk.QuantumCircuit(n)
        for bit in range(n):
            if (j >> bit) & 1:
                qc.x(bit)
        qc.compose(qft_circuit(n), inplace=True)
        qc.compose(inverse_qft_circuit(n), inplace=True)
        sv = qk.quantum_info.Statevector.from_instruction(qc)
        # in Qiskit little-endian, index j in statevector = qubit pattern of j
        prob_j = float(abs(sv.data[j]) ** 2)
        if abs(prob_j - 1.0) > 1e-10:
            ok = False
    # test QFT(|+>^n) = |0>
    qc2 = qk.QuantumCircuit(n)
    qc2.h(range(n))
    qc2.compose(qft_circuit(n), inplace=True)
    sv2 = qk.quantum_info.Statevector.from_instruction(qc2)
    p0 = float(abs(sv2.data[0]) ** 2)
    if abs(p0 - 1.0) > 1e-10:
        ok = False
    status = "PASS" if ok else "FAIL"
    print(f"  verification: roundtrip + QFT(|+>^n)=|0>  [{status}]")


def frequency_demo(n: int) -> None:
    """Show QFT on a state with known frequency content."""
    print(f"\n--- frequency decomposition ({n} qubits) ---\n")

    # input: |j> for j = 2 (a single frequency)
    j_val = 2
    qc_in = qk.QuantumCircuit(n)
    for bit in range(n):
        if (j_val >> bit) & 1:
            qc_in.x(bit)
    print(f"  input state |{j_val}> = ", end="")
    sv_in = qk.quantum_info.Statevector.from_instruction(qc_in)
    print(sv_in.data.round(3))

    qc = qk.QuantumCircuit(n)
    qc.compose(qft_circuit(n), inplace=True)
    sv = sv_in.evolve(qc)
    probs = sv.probabilities_dict()
    print(f"  after QFT (probabilities):")
    for state in sorted(probs.keys()):
        k = int(state[::-1], 2)
        print(f"    |{state}> (k={k})  p = {probs[state]:.4f}  amp = {sv.data[k]:.4f}")


def superposition_demo(n: int) -> None:
    """QFT of the uniform superposition (should give |0>)."""
    print(f"\n--- uniform superposition -> |0> ---\n")
    qc = qk.QuantumCircuit(n)
    qc.h(range(n))
    sv = qk.quantum_info.Statevector.from_instruction(qc)
    qc2 = qk.QuantumCircuit(n)
    qc2.compose(qft_circuit(n), inplace=True)
    sv_out = sv.evolve(qc2)
    probs = sv_out.probabilities_dict()
    print("  QFT(|+>^n) probabilities:")
    for state in sorted(probs.keys()):
        if probs[state] > 0.01:
            print(f"    |{state}>  p = {probs[state]:.4f}")


def iqft_roundtrip(n: int) -> None:
    """Verify QFT then IQFT returns to the original state."""
    print(f"\n--- QFT -> IQFT roundtrip ({n} qubits) ---\n")
    j_val = 3
    qc = qk.QuantumCircuit(n)
    for bit in range(n):
        if (j_val >> bit) & 1:
            qc.x(bit)
    qc.compose(qft_circuit(n), inplace=True)
    qc.compose(inverse_qft_circuit(n), inplace=True)
    sv = qk.quantum_info.Statevector.from_instruction(qc)
    probs = sv.probabilities_dict()
    print(f"  roundtrip |{j_val}> -> QFT -> IQFT:")
    for state in sorted(probs.keys()):
        if probs[state] > 0.01:
            print(f"    |{state}>  p = {probs[state]:.4f}")


def main() -> None:
    for n in (3, 4):
        print(f"=== QFT on {n} qubits ===")
        print("\nverification:")
        verify_qft(n)
        frequency_demo(n)
        superposition_demo(n)
        iqft_roundtrip(n)
        print()

    print("example circuit (3 qubits):")
    print(qft_circuit(3).draw(output="text"))

    backend = qka.AerSimulator()
    n = 3
    qc = qk.QuantumCircuit(n, n)
    qc.x(1)  # prepare |010> = |2>
    qc.compose(qft_circuit(n), inplace=True)
    qc.measure(range(n), range(n))
    counts = backend.run(qk.transpile(qc, backend), shots=4096).result().get_counts()
    print("\nshot histogram for QFT|2> (3 qubits):")
    for bits, cnt in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  |{bits}>  {cnt:4d}")

    print("\n=== done ===")


if __name__ == "__main__":
    main()
