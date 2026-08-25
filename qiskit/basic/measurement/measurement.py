#!/usr/bin/env python3
"""Measurement in Z and X bases.

Demonstrate how the same state gives different measurement statistics
depending on the measurement basis.  Measure in the Z basis (default)
and the X basis (H before measurement).
"""

from __future__ import annotations

import qiskit as qk
import qiskit_aer as qka


def run_statevector(qc: qk.QuantumCircuit) -> qk.quantum_info.Statevector:
    """Return the exact statevector for a circuit."""
    return qk.quantum_info.Statevector.from_instruction(qc)


def run_shots(qc: qk.QuantumCircuit, shots: int = 1000) -> dict[str, int]:
    """Execute a circuit with measurement on Aer and return counts."""
    measured = qc.copy()
    if measured.num_clbits == 0:
        measured.measure_all()
    backend = qka.AerSimulator()
    compiled = qk.transpile(measured, backend)
    return backend.run(compiled, shots=shots).result().get_counts()


def z_basis_measure(state_prep: qk.QuantumCircuit, shots: int = 1000) -> dict[str, int]:
    """Measure qubit in the Z basis (computational basis)."""
    qc = qk.QuantumCircuit(state_prep.num_qubits, state_prep.num_qubits)
    qc.compose(state_prep, inplace=True)
    qc.measure(range(state_prep.num_qubits), range(state_prep.num_qubits))
    backend = qka.AerSimulator()
    compiled = qk.transpile(qc, backend)
    return backend.run(compiled, shots=shots).result().get_counts()


def x_basis_measure(state_prep: qk.QuantumCircuit, shots: int = 1000) -> dict[str, int]:
    """Measure qubit in the X basis (H before measurement)."""
    qc = qk.QuantumCircuit(state_prep.num_qubits, state_prep.num_qubits)
    qc.compose(state_prep, inplace=True)
    qc.h(range(state_prep.num_qubits))
    qc.measure(range(state_prep.num_qubits), range(state_prep.num_qubits))
    backend = qka.AerSimulator()
    compiled = qk.transpile(qc, backend)
    return backend.run(compiled, shots=shots).result().get_counts()


def print_counts(name: str, counts: dict[str, int], shots: int) -> None:
    """Pretty-print measurement counts with fractions."""
    print(f"  {name}:")
    for state in sorted(counts, key=counts.get, reverse=True):  # type: ignore[arg-type]
        frac = counts[state] / shots
        print(f"    |{state}>: {counts[state]:>4}/{shots}  ({frac:.1%})")
    print()


def demo_z0_state() -> None:
    """|0> measured in Z and X bases."""
    print("=== |0> state ===")
    prep = qk.QuantumCircuit(1)
    sv = run_statevector(prep)
    print(f"  statevector: {dict(sv.to_dict())}")

    z_counts = z_basis_measure(prep)
    print_counts("Z-basis", z_counts, 1000)

    x_counts = x_basis_measure(prep)
    print_counts("X-basis", x_counts, 1000)


def demo_x_state() -> None:
    """|+> = H|0> measured in Z and X bases."""
    print("=== |+> = H|0> state ===")
    prep = qk.QuantumCircuit(1)
    prep.h(0)
    sv = run_statevector(prep)
    print(f"  statevector: {dict(sv.to_dict())}")

    z_counts = z_basis_measure(prep)
    print_counts("Z-basis (random 50/50)", z_counts, 1000)

    x_counts = x_basis_measure(prep)
    print_counts("X-basis (deterministic |+>)", x_counts, 1000)


def demo_minus_state() -> None:
    """|-> = HX|0> measured in Z and X bases."""
    print("=== |-> = HX|0> state ===")
    prep = qk.QuantumCircuit(1)
    prep.x(0)
    prep.h(0)
    sv = run_statevector(prep)
    print(f"  statevector: {dict(sv.to_dict())}")

    z_counts = z_basis_measure(prep)
    print_counts("Z-basis (random 50/50)", z_counts, 1000)

    x_counts = x_basis_measure(prep)
    print_counts("X-basis (deterministic |->)", x_counts, 1000)


def demo_one_state() -> None:
    """|1> measured in Z and X bases."""
    print("=== |1> state ===")
    prep = qk.QuantumCircuit(1)
    prep.x(0)
    sv = run_statevector(prep)
    print(f"  statevector: {dict(sv.to_dict())}")

    z_counts = z_basis_measure(prep)
    print_counts("Z-basis", z_counts, 1000)

    x_counts = x_basis_measure(prep)
    print_counts("X-basis (random 50/50)", x_counts, 1000)


def main() -> None:
    demo_z0_state()
    demo_x_state()
    demo_minus_state()
    demo_one_state()


if __name__ == "__main__":
    main()
