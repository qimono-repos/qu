#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=2)


@qml.qnode(dev)
def bell_state() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.state()


@qml.qnode(dev)
def bell_probs() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.probs(wires=[0, 1])


@qml.qnode(dev)
def correlation_z() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.Z(0) @ qml.Z(1))


@qml.qnode(dev)
def correlation_x() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.X(0) @ qml.X(1))


@qml.qnode(dev)
def separate_state() -> qml.typing.Result:
    qml.Hadamard(wires=0)
    return qml.expval(qml.Z(0) @ qml.Z(1))


def main() -> None:
    print("=== Bell State (Entanglement) ===")
    print()
    sv = bell_state()
    probs = bell_probs()
    print(f"|Phi+> = (|00> + |11>)/sqrt(2)")
    print(f"  state: {sv}")
    print(f"  probs: P(|00>) = {probs[0]:.4f}, P(|01>) = {probs[1]:.4f}, "
          f"P(|10>) = {probs[2]:.4f}, P(|11>) = {probs[3]:.4f}")
    print()

    print("=== Correlation Measurements ===")
    print()
    print(f"  <ZZ> = {correlation_z():+.4f}  (expected +1 for Bell state)")
    print(f"  <XX> = {correlation_x():+.4f}  (expected +1 for Bell state)")
    print()

    print("=== Entangled vs Separable ===")
    print()
    print(f"  H|0> on q0 only  <ZZ> = {separate_state():+.4f}  (expected 0, no correlation)")
    print()

    print("=== Measurement Samples (Bell state) ===")
    dev_shots = qml.device("default.qubit", wires=2, shots=4000)

    @qml.qnode(dev_shots)
    def sample_bell() -> qml.typing.Result:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = sample_bell()
    n00 = int(np.sum((samples[:, 0] == 0) & (samples[:, 1] == 0)))
    n01 = int(np.sum((samples[:, 0] == 0) & (samples[:, 1] == 1)))
    n10 = int(np.sum((samples[:, 0] == 1) & (samples[:, 1] == 0)))
    n11 = int(np.sum((samples[:, 0] == 1) & (samples[:, 1] == 1)))
    print(f"  |00>: {n00}  |01>: {n01}  |10>: {n10}  |11>: {n11}")
    print(f"  Only |00> and |11> appear — qubits are perfectly correlated.")


if __name__ == "__main__":
    main()
