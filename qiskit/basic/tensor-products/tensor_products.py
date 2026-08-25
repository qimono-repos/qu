#!/usr/bin/env python3
"""Tensor products of quantum states.

Build multi-qubit systems by composing circuits and inspect the
resulting statevectors.  Show how |a> x |b> appears in the full
computational basis.
"""

from __future__ import annotations

import qiskit as qk
import qiskit_aer as qka


def run_statevector(qc: qk.QuantumCircuit) -> qk.quantum_info.Statevector:
    """Return the exact statevector for a circuit."""
    return qk.quantum_info.Statevector.from_instruction(qc)


def run_shots(qc: qk.QuantumCircuit, shots: int = 1024) -> dict[str, int]:
    """Execute a circuit with measurement on Aer and return counts."""
    measured = qc.copy()
    if measured.num_clbits == 0:
        measured.measure_all()
    backend = qka.AerSimulator()
    compiled = qk.transpile(measured, backend)
    return backend.run(compiled, shots=shots).result().get_counts()


def demo_zero_zero() -> None:
    """|0> tensor |0> = |00>."""
    print("=== |00> (default two-qubit state) ===")
    qc = qk.QuantumCircuit(2)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        print(f"  {a:.4f} |{b}>")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print()


def demo_one_zero() -> None:
    """X|0> tensor |0> = |10>."""
    print("=== |10> (X on qubit 1) ===")
    qc = qk.QuantumCircuit(2)
    qc.x(1)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        if abs(a) > 1e-10:
            print(f"  {a:.4f} |{b}>")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print("Note: qubit 1 is leftmost in the bitstring, qubit 0 is rightmost.")
    print()


def demo_zero_one() -> None:
    """|0> tensor X|0> = |01>."""
    print("=== |01> (X on qubit 0) ===")
    qc = qk.QuantumCircuit(2)
    qc.x(0)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        if abs(a) > 1e-10:
            print(f"  {a:.4f} |{b}>")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print()


def demo_one_one() -> None:
    """X tensor X = |11>."""
    print("=== |11> (X on both qubits) ===")
    qc = qk.QuantumCircuit(2)
    qc.x(0)
    qc.x(1)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        if abs(a) > 1e-10:
            print(f"  {a:.4f} |{b}>")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print()


def demo_superposition_tensor() -> None:
    """|+> tensor |0> = (|00> + |10>)/sqrt(2)."""
    print("=== |+> x |0> = (|00> + |10>)/sqrt(2) ===")
    qc = qk.QuantumCircuit(2)
    qc.h(1)  # H on qubit 1 (left qubit in the diagram)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        if abs(a) > 1e-10:
            print(f"  {a:.4f} |{b}>")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print("The left qubit is in |+>, the right qubit is in |0>.")
    print()


def demo_both_superposition() -> None:
    """|+> tensor |+> = (|00> + |01> + |10> + |11>)/2."""
    print("=== |+> x |+> = (|00> + |01> + |10> + |11>)/2 ===")
    qc = qk.QuantumCircuit(2)
    qc.h(0)
    qc.h(1)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        if abs(a) > 1e-10:
            print(f"  {a:.4f} |{b}>")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print("All four basis states equally likely — product of two 50/50 states.\n")
    print("shots:", run_shots(qc))
    print()


def main() -> None:
    demo_zero_zero()
    demo_one_zero()
    demo_zero_one()
    demo_one_one()
    demo_superposition_tensor()
    demo_both_superposition()


if __name__ == "__main__":
    main()
