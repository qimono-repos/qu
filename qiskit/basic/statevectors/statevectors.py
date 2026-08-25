#!/usr/bin/env python3
"""Statevector inspection with the |+> state.

Create the |+> state, inspect its statevector representation,
and show amplitudes, probabilities, and the full ket decomposition.
"""

from __future__ import annotations

import math

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


def demo_plus_state() -> None:
    """Build |+> = H|0> and inspect the statevector."""
    print("=== |+> = H|0> ===")
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    print(qc.draw(output="text"))

    sv = run_statevector(qc)
    print("raw statevector:", sv.data)
    print("ket decomposition:")
    for bitstring, amp in sv.to_dict().items():
        print(f"  amplitude for |{bitstring}>: {amp}")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print("norm:", round(sum(abs(a) ** 2 for a in sv.data), 6))
    print("shots:", run_shots(qc))
    print()


def demo_minus_state() -> None:
    """Build |-> = HX|0> and inspect."""
    print("=== |-> = HX|0> ===")
    qc = qk.QuantumCircuit(1)
    qc.x(0)
    qc.h(0)
    print(qc.draw(output="text"))

    sv = run_statevector(qc)
    for bitstring, amp in sv.to_dict().items():
        print(f"  amplitude for |{bitstring}>: {amp}")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print()


def demo_plus_i_state() -> None:
    """Build |+i> = HS|0> and inspect."""
    print("=== |+i> = HS|0> ===")
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    qc.s(0)
    print(qc.draw(output="text"))

    sv = run_statevector(qc)
    for bitstring, amp in sv.to_dict().items():
        print(f"  amplitude for |{bitstring}>: {amp}")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print()


def demo_two_qubit_tensor() -> None:
    """Show that tensor product of |+> with |0> gives a 4-element statevector."""
    print("=== tensor product |+> x |0> ===")
    qc = qk.QuantumCircuit(2)
    qc.h(1)  # qubit 1 gets H, qubit 0 stays |0>
    print(qc.draw(output="text"))

    sv = run_statevector(qc)
    print("statevector length:", len(sv.data))
    for bitstring, amp in sv.to_dict().items():
        print(f"  amplitude for |{bitstring}>: {amp}")
    print()


def main() -> None:
    demo_plus_state()
    demo_minus_state()
    demo_plus_i_state()
    demo_two_qubit_tensor()


if __name__ == "__main__":
    main()
