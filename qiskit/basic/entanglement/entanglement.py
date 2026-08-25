#!/usr/bin/env python3
"""Entanglement: Bell states and qubit correlations.

Create the Bell state |Phi+> = (|00> + |11>)/sqrt(2), show the
correlations between qubits, and verify with shot statistics.
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


def bell_circuit() -> qk.QuantumCircuit:
    """Build the Bell state |Phi+> = (|00> + |11>)/sqrt(2)."""
    qc = qk.QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def demo_bell_state() -> None:
    """Create and inspect the Bell state."""
    print("=== Bell state |Phi+> = (|00> + |11>)/sqrt(2) ===")
    qc = bell_circuit()
    print(qc.draw(output="text"))

    sv = run_statevector(qc)
    print("statevector:")
    for b, a in sv.to_dict().items():
        if abs(a) > 1e-10:
            print(f"  {a:.4f} |{b}>")
    print("probabilities:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print()


def demo_correlations() -> None:
    """Show that qubit measurements are perfectly correlated."""
    print("=== Perfect correlations in Bell state ===")
    qc = bell_circuit()
    counts = run_shots(qc, shots=4000)
    print("counts:", counts)
    print("Only |00> and |11> appear — qubits always agree.")
    print(f"  fraction same: {(counts.get('00', 0) + counts.get('11', 0)) / 4000:.1%}")
    print()


def demo_measure_qubit0() -> None:
    """Measure only qubit 0 — qubit 1 still collapses."""
    print("=== Measure qubit 0 only, then inspect qubit 1 ===")
    qc = qk.QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure(0, 0)
    backend = qka.AerSimulator()
    compiled = qk.transpile(qc, backend)
    counts = backend.run(compiled, shots=2000).result().get_counts()
    print("counts (qubit 0 measured):", counts)
    print("After measuring qubit 0, qubit 1 is always the same value.\n")


def demo_bell_states_gallery() -> None:
    """Show all four Bell states."""
    bell_states = {
        "|Phi+>": lambda: _bell(0, "h", "cx"),
        "|Phi->": lambda: _bell(0, "h", "cx", phase_x=0),
        "|Psi+>": lambda: _bell(0, "h", "cx", swap=True),
        "|Psi->": lambda: _bell(0, "h", "cx", swap=True, phase_x=0),
    }

    print("=== Four Bell states ===")
    for name, make in bell_states.items():
        qc = make()
        sv = run_statevector(qc)
        print(f"{name}:")
        for b, a in sv.to_dict().items():
            if abs(a) > 1e-10:
                print(f"  {a:.4f} |{b}>")
        print()


def _bell(
    qubit: int,
    first_gate: str,
    second_gate: str,
    swap: bool = False,
    phase_x: bool = True,
) -> qk.QuantumCircuit:
    """Helper to build a Bell state variant."""
    qc = qk.QuantumCircuit(2)
    if phase_x:
        qc.x(qubit)
    getattr(qc, first_gate)(qubit)
    getattr(qc, second_gate)(qubit, 1 - qubit)
    if swap:
        qc.x(1 - qubit)
    return qc


def main() -> None:
    demo_bell_state()
    demo_correlations()
    demo_measure_qubit0()
    demo_bell_states_gallery()


if __name__ == "__main__":
    main()
