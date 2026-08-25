"""Tensor products: composing multi-qubit states from single-qubit states."""

import numpy as np
import cirq


def main() -> None:
    sim = cirq.Simulator()

    print("=== Tensor Product States ===\n")

    q0, q1 = cirq.LineQubit.range(2)

    states: dict[str, list[cirq.Operation]] = {
        "|0⟩ ⊗ |0⟩": [],
        "|0⟩ ⊗ |1⟩": [cirq.X(q1)],
        "|1⟩ ⊗ |0⟩": [cirq.X(q0)],
        "|1⟩ ⊗ |1⟩": [cirq.X(q0), cirq.X(q1)],
        "|+⟩ ⊗ |0⟩": [cirq.H(q0)],
        "|0⟩ ⊗ |+⟩": [cirq.H(q1)],
        "|+⟩ ⊗ |+⟩": [cirq.H(q0), cirq.H(q1)],
    }

    for label, ops in states.items():
        circuit = cirq.Circuit(ops)
        result = sim.simulate(circuit)
        sv = result.final_state_vector
        print(f"{label}:")
        for i in range(4):
            if abs(sv[i]) > 1e-6:
                print(f"  |{i:02b}⟩: {sv[i]:.4f}  (P = {abs(sv[i])**2:.4f})")

    print("\n=== Tensor product via numpy (manual) ===")
    a = np.array([1, 0], dtype=complex)  # |0⟩
    b = np.array([1, 0], dtype=complex)  # |0⟩
    ab = np.kron(a, b)
    print(f"|0⟩ ⊗ |0⟩ = {ab}")

    a = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)], dtype=complex)  # |+⟩
    b = np.array([1, 0], dtype=complex)  # |0⟩
    ab = np.kron(a, b)
    print(f"|+⟩ ⊗ |0⟩ = {ab}")

    print("\n=== Circuit for |+⟩ ⊗ |1⟩ ===")
    circuit = cirq.Circuit(cirq.X(q1), cirq.H(q0))
    print(circuit)
    result = sim.simulate(circuit)
    print(f"State: {result.final_state_vector}")

    print("\n=== Cirq tensor_product helper ===")
    a = cirq.Circuit(cirq.H(cirq.LineQubit(0)))
    b = cirq.Circuit(cirq.X(cirq.LineQubit(0)))
    combined = cirq.Circuit(cirq.H(q0), cirq.X(q1))
    print(combined)
    print(f"State: {sim.simulate(combined).final_state_vector}")


if __name__ == "__main__":
    main()
