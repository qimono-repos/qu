#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=2)


@qml.qnode(dev)
def cnot_01() -> qml.typing.Result:
    qml.PauliX(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.state()


@qml.qnode(dev)
def cnot_10() -> qml.typing.Result:
    qml.PauliX(wires=1)
    qml.CNOT(wires=[1, 0])
    return qml.state()


@qml.qnode(dev)
def cz_gate() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    qml.CZ(wires=[0, 1])
    return qml.state()


@qml.qnode(dev)
def crz_gate() -> qml.typing.Result:
    qml.PauliX(wires=0)
    qml.Hadamard(wires=1)
    qml.CRZ(np.pi / 4, wires=[0, 1])
    return qml.state()


@qml.qnode(dev)
def flip_flop() -> qml.typing.Result:
    qml.CNOT(wires=[0, 1])
    return qml.state()


def main() -> None:
    print("=== Controlled Gates ===")
    print()

    print("--- CNOT (Controlled-NOT) ---")
    print()
    print("CNOT flips target qubit when control is |1>.")
    print()

    sv = cnot_01()
    print(f"X on q0, then CNOT(0,1):  {sv}")
    print(f"  |10> -> |11> (control q0=1 flips target q1)")
    print()

    sv = cnot_10()
    print(f"X on q1, then CNOT(1,0):  {sv}")
    print(f"  |01> -> |11> (control q1=0 -> no flip)")
    print()

    sv = flip_flop()
    print(f"CNOT on |00>:  {sv}")
    print(f"  |00> -> |00> (control q0=0 -> no flip)")
    print()

    print("--- CZ (Controlled-Z) ---")
    print()
    sv = cz_gate()
    probs = np.abs(sv) ** 2
    print(f"H|0> x H|0>, then CZ:  {sv}")
    print(f"  probs: [{', '.join(f'{p:.4f}' for p in probs)}]")
    print(f"  CZ flips phase of |11> component.")
    print()

    print("--- CRZ (Controlled-Rotation-Z) ---")
    print()
    sv = crz_gate()
    probs = np.abs(sv) ** 2
    print(f"X q0, H q1, CRZ(pi/4):  {sv}")
    print(f"  probs: [{', '.join(f'{p:.4f}' for p in probs)}]")
    print(f"  CRZ applies RZ to target when control is |1>.")


if __name__ == "__main__":
    main()
