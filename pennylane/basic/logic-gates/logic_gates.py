#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)


@qml.qnode(dev)
def apply_x() -> qml.typing.Result:
    qml.PauliX(wires=0)
    return qml.state()


@qml.qnode(dev)
def apply_y() -> qml.typing.Result:
    qml.PauliY(wires=0)
    return qml.state()


@qml.qnode(dev)
def apply_z() -> qml.typing.Result:
    qml.PauliZ(wires=0)
    return qml.state()


@qml.qnode(dev)
def apply_h() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    return qml.state()


@qml.qnode(dev)
def apply_s() -> qml.typing.Result:
    qml.S(wires=0)
    return qml.state()


@qml.qnode(dev)
def apply_t() -> qml.typing.Result:
    qml.T(wires=0)
    return qml.state()


def main() -> None:
    print("=== Quantum Logic Gates (on |0>) ===")
    print()

    gates = [
        ("PauliX (NOT)", apply_x),
        ("PauliY", apply_y),
        ("PauliZ (phase flip)", apply_z),
        ("Hadamard", apply_h),
        ("S (phase)", apply_s),
        ("T (π/8)", apply_t),
    ]

    for label, fn in gates:
        sv = fn()
        probs = np.abs(sv) ** 2
        print(f"{label}:")
        print(f"  state:     {sv}")
        print(f"  probs:     P(|0>) = {probs[0]:.4f},  P(|1>) = {probs[1]:.4f}")
        print()

    print("PauliX flips |0> -> |1>.")
    print("PauliZ flips the phase of |1> but leaves |0> unchanged.")
    print("Hadamard creates equal superposition from |0>.")
    print("S and T are phase gates that rotate the global phase of |1>.")


if __name__ == "__main__":
    main()
