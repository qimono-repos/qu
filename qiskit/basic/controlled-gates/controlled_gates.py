#!/usr/bin/env python3
"""Controlled gates: CNOT, CZ, CY.

Show the truth table for each two-qubit controlled gate by preparing
all four computational-basis inputs and inspecting the output.
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


def truth_table(gate_name: str, gate_fn: callable, num_qubits: int = 2) -> None:
    """Print the truth table for a gate by enumerating all basis inputs."""
    print(f"=== {gate_name} truth table ===")
    print(f"  {'input':>8}  ->  {'output':>8}")
    print(f"  {'--------':>8}     {'--------':>8}")

    for i in range(2 ** num_qubits):
        bits = format(i, f"0{num_qubits}b")
        qc = qk.QuantumCircuit(num_qubits)
        for q in range(num_qubits):
            if bits[num_qubits - 1 - q] == "1":
                qc.x(q)
        gate_fn(qc)
        sv = run_statevector(qc)
        out = next(iter(sv.to_dict()))
        print(f"  |{bits}>  ->  |{out}>")
    print()


def demo_cnot() -> None:
    """CNOT (CX): flips target when control is |1>."""
    def cx_gate(qc: qk.QuantumCircuit) -> None:
        qc.cx(1, 0)  # control=qubit 1, target=qubit 0

    truth_table("CNOT (CX)", cx_gate)
    print("CX flips qubit 0 when qubit 1 is |1>.")
    print("In Qiskit bitstrings: qubit 1 is the left bit, qubit 0 is the right bit.\n")


def demo_cz() -> None:
    """CZ: flips sign of |11> component."""
    print("=== CZ truth table ===")
    print("  CZ is diagonal: it only adds a phase to |11>.")
    print("  |00> -> |00>,  |01> -> |01>,  |10> -> |10>,  |11> -> -|11>\n")

    for i in range(4):
        bits = format(i, "02b")
        qc = qk.QuantumCircuit(2)
        if bits[1] == "1":
            qc.x(1)
        if bits[0] == "1":
            qc.x(0)
        qc.cz(1, 0)
        sv = run_statevector(qc)
        for b, a in sv.to_dict().items():
            if abs(a) > 1e-10:
                print(f"  |{bits}> -> {a:.4f} |{b}>")
    print()


def demo_cy() -> None:
    """CY: applies Y to target when control is |1>."""
    truth_table("CY", lambda qc: qc.cy(1, 0))
    print("CY applies Y to qubit 0 when qubit 1 is |1>.")
    print("Y|0> = i|1>, so |10> -> i|11>.")
    print("Y|1> = -i|0>, so |11> -> -i|10>.\n")


def demo_cnot_shots() -> None:
    """CNOT with superposition input and measurement statistics."""
    print("=== CNOT with H on control ===")
    qc = qk.QuantumCircuit(2, 2)
    qc.h(1)       # put control in superposition
    qc.cx(1, 0)   # CNOT
    qc.measure([1, 0], [1, 0])
    print(qc.draw(output="text"))
    counts = run_shots(qc, shots=2000)
    print("counts:", counts)
    print("Expect |00> and |11> ~50/50 — the Bell state Phi+.\n")


def main() -> None:
    demo_cnot()
    demo_cz()
    demo_cy()
    demo_cnot_shots()


if __name__ == "__main__":
    main()
