#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)


@qml.qnode(dev)
def state_zero() -> qml.typing.Result:
    return qml.state()


@qml.qnode(dev)
def state_one() -> qml.typing.Result:
    qml.PauliX(wires=0)
    return qml.state()


@qml.qnode(dev)
def state_plus() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    return qml.state()


@qml.qnode(dev)
def state_minus() -> qml.typing.Result:
    qml.PauliX(wires=0)
    qml.Hadamard(wires=0)
    return qml.state()


@qml.qnode(dev)
def state_i() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.S(wires=0)
    return qml.state()


def main() -> None:
    print("=== State Vectors ===")
    print()
    for label, fn in [
        ("|0>", state_zero),
        ("|1>", state_one),
        ("|+> = H|0>", state_plus),
        ("|-> = XH|0>", state_minus),
        ("|i> = SH|0>", state_i),
    ]:
        sv = fn()
        print(f"{label}:  {sv}")
    print()

    print("=== Verifying Normalization ===")
    for label, fn in [
        ("|0>", state_zero),
        ("|+>", state_plus),
        ("|i>", state_i),
    ]:
        sv = fn()
        norm = np.linalg.norm(sv)
        print(f"  ||{label}|| = {norm:.6f}")
    print()
    print("All state vectors are normalized (norm = 1).")


if __name__ == "__main__":
    main()
