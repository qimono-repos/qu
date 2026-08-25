"""Inspect state vectors and amplitudes for single-qubit states."""

import numpy as np
import cirq


def main() -> None:
    q = cirq.LineQubit(0)
    sim = cirq.Simulator()

    states: dict[str, list[cirq.Operation]] = {
        "|0⟩": [],
        "|1⟩": [cirq.X(q)],
        "|+⟩": [cirq.H(q)],
        "|-⟩": [cirq.X(q), cirq.H(q)],
        "|i⟩": [cirq.H(q), cirq.S(q)],
        "|-i⟩": [cirq.X(q), cirq.H(q), cirq.S(q)],
    }

    for label, ops in states.items():
        circuit = cirq.Circuit(ops)
        result = sim.simulate(circuit)
        state_vector = result.final_state_vector

        print(f"\n=== {label} ===")
        print(f"Circuit: {circuit}")
        print(f"State vector: {np.array2string(state_vector, precision=4, suppress_small=True)}")
        print("Amplitudes:")
        for i, amp in enumerate(state_vector):
            if abs(amp) > 1e-6:
                print(f"  |{i}⟩: {amp:.4f}  (|amp|² = {abs(amp)**2:.4f})")


if __name__ == "__main__":
    main()
