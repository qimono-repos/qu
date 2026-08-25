#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)


@qml.qnode(dev)
def hadamard_superposition() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    return qml.state()


@qml.qnode(dev)
def hadamard_probs() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    return qml.probs(wires=0)


def main() -> None:
    print("=== Superposition with Hadamard Gate ===")
    print()

    sv = hadamard_superposition()
    probs = hadamard_probs()

    print(f"State after H|0>:  {sv}")
    print(f"Probabilities:     P(|0>) = {probs[0]:.4f},  P(|1>) = {probs[1]:.4f}")
    print()

    print("=== Measurement Statistics (10000 shots) ===")
    dev_shots = qml.device("default.qubit", wires=1, shots=10000)

    @qml.qnode(dev_shots)
    def hadamard_sample() -> qml.typing.Result:
        qml.Hadamard(wires=0)
        return qml.sample(wires=0)

    samples = hadamard_sample()
    n0 = int(np.sum(samples == 0))
    n1 = int(np.sum(samples == 1))
    print(f"  |0> count: {n0} ({100 * n0 / len(samples):.1f}%)")
    print(f"  |1> count: {n1} ({100 * n1 / len(samples):.1f}%)")
    print()

    print("=== Double Hadamard Returns to |0> ===")
    dev2 = qml.device("default.qubit", wires=1)

    @qml.qnode(dev2)
    def double_h() -> qml.typing.Result:
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=0)
        return qml.state()

    sv2 = double_h()
    print(f"H*H|0> = {sv2}")
    print("Applying Hadamard twice returns to the original state.")


if __name__ == "__main__":
    main()
