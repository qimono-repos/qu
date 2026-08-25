#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)


@qml.qnode(dev)
def expval_z() -> qml.typing.Result:
    qml.PauliX(wires=0)
    return qml.expval(qml.Z(0))


@qml.qnode(dev)
def expval_x() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    return qml.expval(qml.X(0))


@qml.qnode(dev)
def probs_state() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    return qml.probs(wires=0)


@qml.qnode(dev)
def measure_z_basis() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.PauliX(wires=0)
    return qml.expval(qml.Z(0))


@qml.qnode(dev)
def measure_x_basis() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    return qml.expval(qml.X(0))


def main() -> None:
    print("=== Expectation Values ===")
    print()
    print(f"<0|Z|0> = {qml.expval(qml.Z(0)).name if False else ''}", end="")
    dev_init = qml.device("default.qubit", wires=1)

    @qml.qnode(dev_init)
    def ez_zero() -> qml.typing.Result:
        return qml.expval(qml.Z(0))

    print(f"<0|Z|0> = {ez_zero():+.4f}  (expected +1)")
    print(f"<1|Z|1> = {expval_z():+.4f}  (expected -1)")
    print(f"<+|X|+> = {expval_x():+.4f}  (expected +1)")
    print()

    print("=== Probabilities ===")
    probs = probs_state()
    print(f"H|0>  P(|0>) = {probs[0]:.4f},  P(|1>) = {probs[1]:.4f}")
    print()

    print("=== Measurement in Different Bases ===")
    print()
    print("Measuring X|0> in the Z-basis (after H):")
    print(f"  <X|0> = {measure_z_basis():+.4f}  (expected 0)")
    print()
    print("Measuring H|0> in the X-basis:")
    print(f"  <+|H|0> = {measure_x_basis():+.4f}  (expected 1)")
    print()

    print("=== Multi-measurement with samples ===")
    dev_shots = qml.device("default.qubit", wires=1, shots=4000)

    @qml.qnode(dev_shots)
    def sample_hadamard() -> qml.typing.Result:
        qml.Hadamard(wires=0)
        return qml.sample(wires=0)

    samples = sample_hadamard()
    print(f"H|0> measured 4000 times: {int(np.sum(samples == 0))} zeros, "
          f"{int(np.sum(samples == 1))} ones (expect ~50/50)")


if __name__ == "__main__":
    main()
