"""Single-qubit logic gates: X, Y, Z, H, S, T with state transformations."""

import numpy as np
import cirq


def main() -> None:
    q = cirq.LineQubit(0)
    sim = cirq.Simulator()

    gates: list[tuple[str, cirq.Gate, list[cirq.Operation]]] = [
        ("X (bit-flip)", cirq.X, [cirq.X(q)]),
        ("Y", cirq.Y, [cirq.Y(q)]),
        ("Z (phase-flip)", cirq.Z, [cirq.Z(q)]),
        ("H (Hadamard)", cirq.H, [cirq.H(q)]),
        ("S (√Z)", cirq.S, [cirq.S(q)]),
        ("T (√S)", cirq.T, [cirq.T(q)]),
    ]

    print("=== Starting from |0⟩ ===\n")
    for name, gate, ops in gates:
        circuit = cirq.Circuit(ops)
        result = sim.simulate(circuit)
        sv = result.final_state_vector
        print(f"{name}:")
        print(f"  Matrix:\n{np.array2string(np.array(gate.unitary()), precision=3)}")
        print(f"  State: {np.array2string(sv, precision=4)}")
        print(f"  |0⟩ amp: {sv[0]:.4f},  |1⟩ amp: {sv[1]:.4f}")
        print()

    print("=== Combining gates: T† S H |0⟩ ===")
    circuit = cirq.Circuit([cirq.H(q), cirq.S(q), cirq.T(q) ** -1])
    result = sim.simulate(circuit)
    print(circuit)
    print(f"State: {result.final_state_vector}")


if __name__ == "__main__":
    main()
