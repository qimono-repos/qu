#!/usr/bin/env python3
"""Deutsch-Jozsa algorithm — distinguish constant from balanced oracles, n=2."""
import pennylane as qml
import numpy as np

N = 2
dev = qml.device("default.qubit", wires=N + 1)


def oracle_constant_zero():
    """Constant f(x) = 0: does nothing."""
    pass


def oracle_constant_one():
    """Constant f(x) = 1: flips the output qubit."""
    qml.PauliX(wires=N)


def oracle_balanced_identity():
    """Balanced f(x) = x₀: CNOT from qubit 0 to output."""
    qml.CNOT(wires=[0, N])


def oracle_balanced_not():
    """Balanced f(x) = NOT x₀: X then CNOT."""
    qml.PauliX(wires=0)
    qml.CNOT(wires=[0, N])
    qml.PauliX(wires=0)


@qml.qnode(dev)
def deutsch_jozsa_circuit(oracle_fn) -> qml.typing.Result:
    """Deutsch-Jozsa: if all top qubits are |0⟩ after query, f is constant."""
    qml.PauliX(wires=N)
    qml.Hadamard(wires=range(N + 1))
    oracle_fn()
    qml.Hadamard(wires=range(N))
    return qml.probs(wires=range(N))


def classify(probs: np.ndarray) -> str:
    """If measurement is all-zeros, function is constant; otherwise balanced."""
    if np.isclose(probs[0], 1.0):
        return "constant"
    return "balanced"


def main() -> None:
    print("=== Deutsch-Jozsa Algorithm (n=2) ===")
    print(f"Using {N} input qubits + 1 output qubit")
    print()

    oracles = [
        ("f(x) = 0 (constant)", oracle_constant_zero),
        ("f(x) = 1 (constant)", oracle_constant_one),
        ("f(x) = x₀ (balanced)", oracle_balanced_identity),
        ("f(x) = ¬x₀ (balanced)", oracle_balanced_not),
    ]

    for name, oracle_fn in oracles:
        probs = deutsch_jozsa_circuit(oracle_fn)
        result = classify(probs)
        measured = np.argmax(probs)
        measured_bits = format(measured, f"0{N}b")
        print(f"  Oracle: {name}")
        print(f"    Measurement probs: {probs}")
        print(f"    Measured: |{measured_bits}⟩  →  {result}")
        print()

    print("With a classical approach, 2^(n-1)+1 queries are needed.")
    print("Deutsch-Jozsa solves it in just 1 query.")


if __name__ == "__main__":
    main()
