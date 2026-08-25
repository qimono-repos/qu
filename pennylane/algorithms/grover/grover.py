#!/usr/bin/env python3
"""Grover search on 3 qubits — find |101⟩."""
import pennylane as qml
import numpy as np

N_QUBITS = 3
TARGET = "101"
dev = qml.device("default.qubit", wires=N_QUBITS)


def oracle():
    """Mark |101⟩ by flipping its phase with multi-controlled Z."""
    for w in range(N_QUBITS):
        if TARGET[w] == "0":
            qml.PauliX(wires=w)
    qml.Hadamard(wires=N_QUBITS - 1)
    qml.ctrl(qml.PauliX, control=range(N_QUBITS - 1))(wires=N_QUBITS - 1)
    qml.Hadamard(wires=N_QUBITS - 1)
    for w in range(N_QUBITS):
        if TARGET[w] == "0":
            qml.PauliX(wires=w)


def diffusion():
    """Grover diffusion operator: 2|s⟩⟨s| - I."""
    qml.Hadamard(wires=range(N_QUBITS))
    qml.PauliX(wires=range(N_QUBITS))
    qml.Hadamard(wires=N_QUBITS - 1)
    qml.ctrl(qml.PauliX, control=range(N_QUBITS - 1))(wires=N_QUBITS - 1)
    qml.Hadamard(wires=N_QUBITS - 1)
    qml.PauliX(wires=range(N_QUBITS))
    qml.Hadamard(wires=range(N_QUBITS))


@qml.qnode(dev)
def grover_circuit() -> qml.typing.Result:
    """Grover search with optimal iterations for N=8, M=1: ⌊π√8/4⌋ = 2."""
    qml.Hadamard(wires=range(N_QUBITS))
    for _ in range(2):
        oracle()
        diffusion()
    return qml.probs(wires=range(N_QUBITS))


def main() -> None:
    print(f"=== Grover Search for |{TARGET}⟩ (3 qubits) ===")
    print(f"Search space: N = {2**N_QUBITS},  Target: M = 1")
    print(f"Optimal iterations: ⌊π√N / 4⌋ = 2")
    print()

    print("Circuit:")
    print(qml.draw(grover_circuit)())
    print()

    probs = grover_circuit()
    target_idx = int(TARGET, 2)
    print(f"  |{TARGET}⟩ probability = {probs[target_idx]:.4f}")
    print()

    labels = [f"|{i:0{N_QUBITS}b}⟩" for i in range(2**N_QUBITS)]
    for label, p in zip(labels, probs):
        marker = "  <-- peak" if p > 0.5 else ""
        print(f"  {label}  {p:.4f}{marker}")


if __name__ == "__main__":
    main()
