#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)


@qml.qnode(dev)
def circuit_zero() -> qml.typing.Result:
    return qml.probs(wires=0)


@qml.qnode(dev)
def circuit_one() -> qml.typing.Result:
    qml.PauliX(wires=0)
    return qml.probs(wires=0)


@qml.qnode(dev)
def circuit_sample_zero() -> qml.typing.Result:
    return qml.sample(wires=0)


@qml.qnode(dev)
def circuit_sample_one() -> qml.typing.Result:
    qml.PauliX(wires=0)
    return qml.sample(wires=0)


def main() -> None:
    p0 = circuit_zero()
    p1 = circuit_one()

    print("=== Computational Basis States ===")
    print()
    print(f"|0> probabilities:  P(|0>) = {p0[0]:.4f},  P(|1>) = {p0[1]:.4f}")
    print(f"|1> probabilities:  P(|0>) = {p1[0]:.4f},  P(|1>) = {p1[1]:.4f}")
    print()

    s0 = circuit_sample_zero()
    s1 = circuit_sample_one()

    print("=== Measurement Samples (1000 shots) ===")
    dev_shots = qml.device("default.qubit", wires=1, shots=1000)

    @qml.qnode(dev_shots)
    def sample_zero() -> qml.typing.Result:
        return qml.sample(wires=0)

    @qml.qnode(dev_shots)
    def sample_one() -> qml.typing.Result:
        qml.PauliX(wires=0)
        return qml.sample(wires=0)

    samples_zero = sample_zero()
    samples_one = sample_one()

    print(f"|0> samples:  {np.sum(samples_zero == 0)} zeros, {np.sum(samples_zero == 1)} ones")
    print(f"|1> samples:  {np.sum(samples_one == 0)} zeros, {np.sum(samples_one == 1)} ones")
    print()
    print("The |0> state always measures 0; the |1> state always measures 1.")


if __name__ == "__main__":
    main()
