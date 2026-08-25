"""Phase kickback: eigenvalue kickback through controlled operations."""

import cirq
import numpy as np


def main() -> None:
    q0, q1 = cirq.LineQubit.range(2)
    sim = cirq.Simulator()

    print("=== Phase Kickback with CNOT ===\n")
    print("Control in |+⟩, target in |1⟩ → CNOT kicks phase to control.\n")

    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.X(q1),
        cirq.CNOT(q0, q1),
    )
    print(circuit)
    result = sim.simulate(circuit)
    sv = result.final_state_vector
    print(f"State: {np.array2string(sv, precision=3)}")
    print("Result: (|0⟩|1⟩ - |1⟩|0⟩)/√2 — the |1⟩ on q0 picked up a -1 phase.\n")

    print("=== Phase Kickback with CZ ===\n")
    print("Both qubits in |+⟩ → CZ kicks -1 phase to control.\n")

    circuit2 = cirq.Circuit(
        cirq.H(q0),
        cirq.H(q1),
        cirq.CZ(q0, q1),
    )
    print(circuit2)
    result2 = sim.simulate(circuit2)
    sv2 = result2.final_state_vector
    print(f"State: {np.array2string(sv2, precision=3)}")
    print("The |++⟩ state picks up a -1 phase on |11⟩ → (|0+⟩ - |1-⟩)/√2 on control.\n")

    print("=== Phase Kickback in Oracle Search ===\n")
    print("Apply oracle to |+⟩⊗n, measure all in Hadamard basis.\n")

    q0, q1 = cirq.LineQubit.range(2)
    grover_prep = cirq.Circuit(
        cirq.H(q0),
        cirq.H(q1),
        cirq.CZ(q0, q1),
        cirq.H(q0),
        cirq.H(q1),
    )
    print(grover_prep)
    result3 = sim.simulate(grover_prep)
    sv3 = result3.final_state_vector
    probs3 = np.abs(sv3) ** 2
    for i in range(4):
        print(f"  P(|{i:02b}⟩) = {probs3[i]:.4f}")

    print("\n=== Eigenvalue Kickback (T gate) ===\n")
    print("Control in |+⟩, target in eigenstate |1⟩ of T gate.\n")
    circuit_t = cirq.Circuit(
        cirq.H(q0),
        cirq.X(q1),
        cirq.CNOT(q0, q1),
        cirq.T(q1),
        cirq.CNOT(q0, q1),
    )
    print(circuit_t)
    result_t = sim.simulate(circuit_t)
    sv_t = result_t.final_state_vector
    print(f"State: {np.array2string(sv_t, precision=3)}")
    print("Control qubit picks up T gate eigenvalue when target is |1⟩.")


if __name__ == "__main__":
    main()
