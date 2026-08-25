#!/usr/bin/env python3
"""Phase kickback — the eigenvalue is kicked into the ancilla qubit."""
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=2)


@qml.qnode(dev)
def phase_kickback_circuit(theta: float) -> qml.typing.Result:
    """Apply a controlled-U with |−⟩ ancilla to observe phase kickback.

    When the target is an eigenstate |u⟩ of U with eigenvalue e^{iθ},
    the ancilla picks up the phase: |0⟩|u⟩ → e^{iθ}|0⟩|u⟩ after kickback.
    """
    qml.Hadamard(wires=0)
    qml.PauliX(wires=1)
    qml.Hadamard(wires=1)
    qml.ctrl(qml.RZ, control=0)(theta, wires=1)
    qml.Hadamard(wires=0)
    return qml.state()


@qml.qnode(dev)
def compare_no_kickback(theta: float) -> qml.typing.Result:
    """Same circuit but ancilla starts in |0⟩ — no kickback visible."""
    qml.Hadamard(wires=0)
    qml.ctrl(qml.RZ, control=0)(theta, wires=1)
    qml.Hadamard(wires=0)
    return qml.state()


def main() -> None:
    print("=== Phase Kickback Demonstration ===")
    print()

    thetas = [np.pi / 4, np.pi / 2, np.pi]
    for theta in thetas:
        print(f"θ = {theta:.4f}  ({theta / np.pi:.4f}π)")
        print()

        print("  With |−⟩ ancilla (phase kickback):")
        print(qml.draw(phase_kickback_circuit)(theta))
        state = phase_kickback_circuit(theta)
        print(f"    State: {state}")
        print(f"    |00⟩ amp = {state[0]:.4f},  |01⟩ amp = {state[1]:.4f}")
        print(f"    |10⟩ amp = {state[2]:.4f},  |11⟩ amp = {state[3]:.4f}")
        print()

        print("  With |0⟩ ancilla (no kickback):")
        state0 = compare_no_kickback(theta)
        print(f"    State: {state0}")
        print(f"    P(ancilla=0) = {abs(state0[0])**2 + abs(state0[1])**2:.4f}")
        print(f"    P(ancilla=1) = {abs(state0[2])**2 + abs(state0[3])**2:.4f}")
        print()

    print("Key insight: with |−⟩ ancilla the target is unchanged and")
    print("the phase appears as a relative phase on the ancilla |0⟩/|1⟩.")
    print("This is the mechanism behind quantum phase estimation and Grover.")


if __name__ == "__main__":
    main()
