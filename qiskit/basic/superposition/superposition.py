#!/usr/bin/env python3
"""Superposition with Hadamard, then entanglement with CX.

This file is a self-contained Bell-pair walkthrough. It does not import
any helpers from the logic-gates or toffoli folders.
"""

from __future__ import annotations

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, partial_trace, entropy
from qiskit_aer import AerSimulator


SHOTS = 4096


def single_qubit_superposition() -> QuantumCircuit:
    """Put one qubit on the equator of the Bloch sphere: H|0> = |+>."""
    qc = QuantumCircuit(1, 1, name="plus")
    qc.h(0)
    qc.measure(0, 0)
    return qc


def bell_phi_plus() -> QuantumCircuit:
    """Build |Phi+> = (|00> + |11>)/sqrt(2) with H then CX."""
    qc = QuantumCircuit(2, name="phi_plus")
    qc.h(0)
    qc.cx(0, 1)
    return qc


def bell_psi_minus() -> QuantumCircuit:
    """A different Bell state, built from scratch: (|01> - |10>)/sqrt(2)."""
    qc = QuantumCircuit(2, name="psi_minus")
    qc.x(1)
    qc.h(0)
    qc.z(0)
    qc.cx(0, 1)
    return qc


def show_state(title: str, qc: QuantumCircuit) -> None:
    sv = Statevector.from_instruction(qc)
    print(title)
    print(qc.draw(output="text"))
    for bits, amp in sv.to_dict().items():
        if abs(amp) > 1e-12:
            print(f"  {amp.real:+.4f}{amp.imag:+.4f}j  |{bits}>")
    reduced = partial_trace(sv, [1])
    print(f"  von Neumann entropy of qubit 0: {entropy(reduced, base=2):.4f} bits")
    print()


def sample_bell(qc: QuantumCircuit) -> dict[str, int]:
    measured = qc.copy()
    measured.measure_all()
    backend = AerSimulator()
    compiled = transpile(measured, backend)
    return backend.run(compiled, shots=SHOTS).result().get_counts()


def correlation(counts: dict[str, int]) -> float:
    """P(bits equal) - P(bits different) for a two-qubit shot histogram."""
    agree = disagree = 0
    for bitstring, n in counts.items():
        bits = bitstring.replace(" ", "")
        if bits[0] == bits[1]:
            agree += n
        else:
            disagree += n
    total = agree + disagree
    return (agree - disagree) / total


def main() -> None:
    plus = single_qubit_superposition()
    print("=== single-qubit superposition (Hadamard) ===")
    print(plus.draw(output="text"))
    backend = AerSimulator()
    plus_counts = backend.run(transpile(plus, backend), shots=SHOTS).result().get_counts()
    print(f"shots={SHOTS}: {plus_counts}")
    print("expect roughly half |0> and half |1>\n")

    phi = bell_phi_plus()
    show_state("=== Bell |Phi+> via H then CX ===", phi)
    phi_counts = sample_bell(phi)
    print(f"|Phi+> shots={SHOTS}: {phi_counts}")
    print(f"|Phi+> ZZ correlation: {correlation(phi_counts):+.3f}")
    print("only |00> and |11> should appear — the qubits are entangled\n")

    psi = bell_psi_minus()
    show_state("=== Bell |Psi-> (independent circuit) ===", psi)
    psi_counts = sample_bell(psi)
    print(f"|Psi-> shots={SHOTS}: {psi_counts}")
    print(f"|Psi-> ZZ correlation: {correlation(psi_counts):+.3f}")


if __name__ == "__main__":
    main()
