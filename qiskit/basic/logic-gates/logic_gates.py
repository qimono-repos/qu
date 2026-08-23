#!/usr/bin/env python3
"""Basic quantum logic gates as standalone Qiskit circuits.

Each gate is applied to a computational-basis input and simulated
exactly with Statevector, then (for the multi-qubit gates) with shots
on Aer. Nothing here is imported from the other example folders.
"""

from __future__ import annotations

import qiskit as qk
from qiskit_aer import AerSimulator


def ket_label(sv: qk.quantum_info.Statevector, cutoff: float = 1e-10) -> str:
    """Pretty-print a statevector as a sum of computational-basis kets."""
    pieces: list[str] = []
    for bitstring, amp in sv.to_dict().items():
        if abs(amp) < cutoff:
            continue
        pieces.append(f"({amp.real:+.3f}{amp.imag:+.3f}j)|{bitstring}>")
    return " + ".join(pieces) if pieces else "0"


def run_statevector(qc: qk.QuantumCircuit) -> qk.quantum_info.Statevector:
    return qk.quantum_info.Statevector.from_instruction(qc)


def run_shots(qc: qk.QuantumCircuit, shots: int = 1024) -> dict[str, int]:
    measured = qc.copy()
    if measured.num_clbits == 0:
        measured.measure_all()
    backend = AerSimulator()
    compiled = qk.transpile(measured, backend)
    return backend.run(compiled, shots=shots).result().get_counts()


def demo_pauli_x() -> None:
    print("=== Pauli-X (NOT) on |0> ===")
    qc = qk.QuantumCircuit(1)
    qc.x(0)
    print(qc.draw(output="text"))
    print("state:", ket_label(run_statevector(qc)))
    print()


def demo_pauli_y_and_z() -> None:
    print("=== Pauli-Y on |0> and Pauli-Z on |+> ===")
    y_on_zero = qk.QuantumCircuit(1)
    y_on_zero.y(0)
    print("Y|0> =", ket_label(run_statevector(y_on_zero)))

    plus = qk.QuantumCircuit(1)
    plus.h(0)
    print("H|0> = |+> =", ket_label(run_statevector(plus)))

    z_on_plus = qk.QuantumCircuit(1)
    z_on_plus.h(0)
    z_on_plus.z(0)
    print("Z|+> = |-> =", ket_label(run_statevector(z_on_plus)))
    print()


def demo_phase_gates() -> None:
    print("=== S and T phase gates on |+> ===")
    s_circ = qk.QuantumCircuit(1)
    s_circ.h(0)
    s_circ.s(0)
    print("S|+> =", ket_label(run_statevector(s_circ)))

    t_circ = qk.QuantumCircuit(1)
    t_circ.h(0)
    t_circ.t(0)
    print("T|+> =", ket_label(run_statevector(t_circ)))
    print()


def demo_hadamard() -> None:
    print("=== Hadamard on |0> and |1> ===")
    h0 = qk.QuantumCircuit(1)
    h0.h(0)
    print("H|0> =", ket_label(run_statevector(h0)))

    h1 = qk.QuantumCircuit(1)
    h1.x(0)
    h1.h(0)
    print("H|1> =", ket_label(run_statevector(h1)))
    print("H|0> shots:", run_shots(h0))
    print()


def demo_cx_truth_table() -> None:
    print("=== CX truth table (control=q1, target=q0; Qiskit prints q1 q0) ===")
    for control, target in ((0, 0), (0, 1), (1, 0), (1, 1)):
        qc = qk.QuantumCircuit(2)
        if target:
            qc.x(0)
        if control:
            qc.x(1)
        qc.cx(1, 0)
        bits = next(iter(run_statevector(qc).to_dict()))
        print(f"  |{control}{target}>  --CX-->  |{bits}>")
    print()


def demo_swap() -> None:
    print("=== SWAP of |10> ===")
    qc = qk.QuantumCircuit(2)
    qc.x(1)
    print("before:", ket_label(run_statevector(qc)))
    qc.swap(0, 1)
    print("after: ", ket_label(run_statevector(qc)))
    print(qc.draw(output="text"))
    print()


def main() -> None:
    demo_pauli_x()
    demo_pauli_y_and_z()
    demo_phase_gates()
    demo_hadamard()
    demo_cx_truth_table()
    demo_swap()


if __name__ == "__main__":
    main()
