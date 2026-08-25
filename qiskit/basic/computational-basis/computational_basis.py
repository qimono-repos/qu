#!/usr/bin/env python3
"""Computational-basis states |0> and |1>.

Prepare both basis states, inspect their statevectors, measure them,
and show that measurement collapses the state with certainty.
"""

from __future__ import annotations

import qiskit as qk
import qiskit_aer as qka


def run_statevector(qc: qk.QuantumCircuit) -> qk.quantum_info.Statevector:
    """Return the exact statevector for a circuit (no measurement)."""
    return qk.quantum_info.Statevector.from_instruction(qc)


def run_shots(qc: qk.QuantumCircuit, shots: int = 1024) -> dict[str, int]:
    """Execute a circuit with measurement on Aer and return counts."""
    measured = qc.copy()
    if measured.num_clbits == 0:
        measured.measure_all()
    backend = qka.AerSimulator()
    compiled = qk.transpile(measured, backend)
    return backend.run(compiled, shots=shots).result().get_counts()


def ket_label(sv: qk.quantum_info.Statevector, cutoff: float = 1e-10) -> str:
    """Pretty-print a statevector as a sum of computational-basis kets."""
    pieces: list[str] = []
    for bitstring, amp in sv.to_dict().items():
        if abs(amp) < cutoff:
            continue
        pieces.append(f"({amp.real:+.3f}{amp.imag:+.3f}j)|{bitstring}>")
    return " + ".join(pieces) if pieces else "0"


def demo_zero_state() -> None:
    """Show the |0> state: default qubit after init."""
    print("=== |0> state (qubit default) ===")
    qc = qk.QuantumCircuit(1)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    print("state:", ket_label(sv))
    probs = sv.probabilities_dict()
    print("probabilities:", {k: round(v, 4) for k, v in probs.items()})
    print("shots:", run_shots(qc))
    print()


def demo_one_state() -> None:
    """Show the |1> state: flip with X gate."""
    print("=== |1> state (X gate) ===")
    qc = qk.QuantumCircuit(1)
    qc.x(0)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    print("state:", ket_label(sv))
    probs = sv.probabilities_dict()
    print("probabilities:", {k: round(v, 4) for k, v in probs.items()})
    print("shots:", run_shots(qc))
    print()


def demo_superposition() -> None:
    """Show equal superposition via Hadamard for contrast."""
    print("=== (|0> + |1>)/sqrt(2) via Hadamard ===")
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    print("state:", ket_label(sv))
    probs = sv.probabilities_dict()
    print("probabilities:", {k: round(v, 4) for k, v in probs.items()})
    print("shots:", run_shots(qc))
    print()


def main() -> None:
    demo_zero_state()
    demo_one_state()
    demo_superposition()


if __name__ == "__main__":
    main()
