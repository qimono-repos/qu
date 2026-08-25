"""Controlled gates: CNOT and CZ with truth tables."""

import cirq
import numpy as np


def print_truth_table(gate_name: str, gate: cirq.Gate, num_qubits: int = 2) -> None:
    """Print the truth table for a two-qubit gate."""
    sim = cirq.Simulator()
    q0, q1 = cirq.LineQubit.range(num_qubits)

    print(f"\n=== {gate_name} Truth Table ===\n")
    print(f"{'Input':<12} {'Output':<12} {'State Vector'}")
    print("-" * 50)

    for a in range(2):
        for b in range(2):
            ops: list[cirq.Operation] = []
            if a:
                ops.append(cirq.X(q0))
            if b:
                ops.append(cirq.X(q1))
            ops.append(gate(q0, q1))

            result = sim.simulate(cirq.Circuit(ops))
            sv = result.final_state_vector
            out_state = np.argmax(np.abs(sv))
            out_binary = format(out_state, f"0{num_qubits}b")
            print(f"|{a}{b}⟩          |{out_binary}⟩          {np.array2string(sv, precision=3)}")


def main() -> None:
    print_truth_table("CNOT (CX)", cirq.CNOT)
    print_truth_table("CZ", cirq.CZ)

    print("\n=== Matrix Representations ===\n")
    for name, gate in [("CNOT", cirq.CNOT), ("CZ", cirq.CZ)]:
        print(f"{name} matrix:")
        print(np.array2string(np.array(gate.unitary()), precision=0))
        print()

    print("=== Circuit Diagrams ===")
    q0, q1 = cirq.LineQubit.range(2)
    print(f"\nCNOT: {cirq.Circuit(cirq.CNOT(q0, q1))}")
    print(f"CZ:   {cirq.Circuit(cirq.CZ(q0, q1))}")

    print("\n=== Reversed CNOT (control=q1, target=q0) ===")
    print(cirq.Circuit(cirq.CNOT(q1, q0)))

    print("\n=== Toffoli (3-qubit controlled-CNOT) ===")
    q0, q1, q2 = cirq.LineQubit.range(3)
    print(cirq.Circuit(cirq.CCX(q0, q1, q2)))


if __name__ == "__main__":
    main()
