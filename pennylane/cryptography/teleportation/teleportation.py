#!/usr/bin/env python3
"""Quantum teleportation using PennyLane."""

from __future__ import annotations

import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=3)


@qml.qnode(dev)
def teleport_circuit(theta: float, phi: float) -> np.ndarray:
    qml.RY(theta, wires=0)
    qml.RZ(phi, wires=0)

    qml.Hadamard(wires=1)
    qml.CNOT(wires=[1, 2])

    qml.CNOT(wires=[0, 1])
    qml.Hadamard(wires=0)

    qml.CNOT(wires=[1, 2])
    qml.CZ(wires=[0, 2])

    return qml.probs(wires=2)


@qml.qnode(dev)
def original_state(theta: float, phi: float) -> np.ndarray:
    qml.RY(theta, wires=0)
    qml.RZ(phi, wires=0)
    return qml.probs(wires=0)


def main() -> None:
    print("=== Quantum Teleportation (PennyLane) ===\n")

    for name, theta, phi in [("|0>", 0, 0), ("|1>", np.pi, 0), ("|+>", np.pi / 2, 0), ("arbitrary", 0.7, 1.2)]:
        print(f"Teleporting {name} (theta={theta:.2f}, phi={phi:.2f}):")
        orig = original_state(theta, phi)
        teleported = teleport_circuit(theta, phi)
        print(f"  Original:    |0>={orig[0]:.4f}, |1>={orig[1]:.4f}")
        print(f"  Teleported:  |0>={teleported[0]:.4f}, |1>={teleported[1]:.4f}")
        match = np.allclose(orig, teleported, atol=0.05)
        print(f"  Match: {match}\n")

    print(qml.draw(teleport_circuit)(0.7, 1.2))


if __name__ == "__main__":
    main()
