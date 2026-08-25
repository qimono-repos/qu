#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=2)


@qml.qnode(dev)
def tensor_zero_zero() -> qml.typing.Result:
    return qml.state()


@qml.qnode(dev)
def tensor_zero_one() -> qml.typing.Result:
    qml.PauliX(wires=1)
    return qml.state()


@qml.qnode(dev)
def tensor_one_zero() -> qml.typing.Result:
    qml.PauliX(wires=0)
    return qml.state()


@qml.qnode(dev)
def tensor_plus_plus() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    return qml.state()


@qml.qnode(dev)
def tensor_plus_zero() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    return qml.state()


def main() -> None:
    print("=== Tensor Products of Two-Qubit States ===")
    print()
    print("Qubit 0 = leftmost, Qubit 1 = rightmost in the state vector.")
    print("Basis order: |00>, |01>, |10>, |11>")
    print()

    states = [
        ("|0>|0>", tensor_zero_zero),
        ("|0>|1>", tensor_zero_one),
        ("|1>|0>", tensor_one_zero),
        ("|+>|+>", tensor_plus_plus),
        ("|+>|0>", tensor_plus_zero),
    ]

    for label, fn in states:
        sv = fn()
        probs = np.abs(sv) ** 2
        print(f"{label}:")
        print(f"  state: {sv}")
        print(f"  probs: [{', '.join(f'{p:.4f}' for p in probs)}]")
        print()

    print("=== Verifying Kronecker Product ===")
    print()
    h_state = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)])
    z0 = np.array([1, 0])

    kron_result = np.kron(h_state, z0)
    sv = tensor_plus_zero()
    print(f"|+>|0> via kron:     {kron_result}")
    print(f"|+>|0> via circuit:  {sv}")
    print(f"Match: {np.allclose(kron_result, sv)}")


if __name__ == "__main__":
    main()
