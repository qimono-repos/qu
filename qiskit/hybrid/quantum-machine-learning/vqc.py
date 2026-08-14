#!/usr/bin/env python3
"""Hybrid variational quantum classifier for a 2-bit XOR dataset.

A tiny ZZ-style feature map plus a 2-qubit variational block is trained
by a classical optimiser (COBYLA) that only ever sees a scalar loss.
The quantum piece never talks to the QAOA or TSP snippets.
"""

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.optimize import minimize


# XOR: linearly inseparable, so a classical perceptron cannot solve it.
FEATURES = np.array(
    [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0],
    ]
)
LABELS = np.array([0, 1, 1, 0])
N_QUBITS = 2
N_PARAMS = 8
# ZZ is the parity observable: +1 when the two bits agree, -1 when they differ.
PARITY = SparsePauliOp("ZZ")


def feature_map(x: np.ndarray) -> QuantumCircuit:
    """ZZ feature map: Hadamards, data phases, then an entangling product phase."""
    x0 = np.pi * float(x[0])
    x1 = np.pi * float(x[1])
    qc = QuantumCircuit(N_QUBITS, name="fmap")
    qc.h(0)
    qc.h(1)
    qc.rz(x0, 0)
    qc.rz(x1, 1)
    qc.cx(0, 1)
    qc.rz(x0 * x1 / np.pi, 1)
    qc.cx(0, 1)
    return qc


def variational_block(theta: np.ndarray) -> QuantumCircuit:
    """Hardware-efficient ansatz: RY layers separated by CX, 8 angles."""
    qc = QuantumCircuit(N_QUBITS, name="ansatz")
    qc.ry(float(theta[0]), 0)
    qc.ry(float(theta[1]), 1)
    qc.cx(0, 1)
    qc.ry(float(theta[2]), 0)
    qc.ry(float(theta[3]), 1)
    qc.cx(1, 0)
    qc.ry(float(theta[4]), 0)
    qc.ry(float(theta[5]), 1)
    qc.cx(0, 1)
    qc.ry(float(theta[6]), 0)
    qc.ry(float(theta[7]), 1)
    return qc


def bound_circuit(x: np.ndarray, theta: np.ndarray) -> QuantumCircuit:
    qc = QuantumCircuit(N_QUBITS)
    qc.compose(feature_map(x), inplace=True)
    qc.compose(variational_block(theta), inplace=True)
    return qc


def predict_score(x: np.ndarray, theta: np.ndarray) -> float:
    """Map <ZZ> in [-1, 1] to a [0, 1] XOR score (1 means the bits differ)."""
    exp_zz = Statevector.from_instruction(bound_circuit(x, theta)).expectation_value(PARITY)
    return 0.5 * (1.0 - float(np.real(exp_zz)))


def predict_label(x: np.ndarray, theta: np.ndarray) -> int:
    return int(predict_score(x, theta) >= 0.5)


def mse_loss(theta: np.ndarray) -> float:
    scores = np.array([predict_score(x, theta) for x in FEATURES])
    return float(np.mean((scores - LABELS) ** 2))


def accuracy(theta: np.ndarray) -> float:
    hits = [predict_label(x, theta) == y for x, y in zip(FEATURES, LABELS)]
    return float(np.mean(hits))


def main() -> None:
    print("hybrid VQC on the XOR truth table")
    print("features -> label")
    for x, y in zip(FEATURES, LABELS):
        print(f"  {tuple(x.tolist())} -> {y}")
    print()

    rng = np.random.default_rng(4)
    seed = rng.uniform(0.0, 2.0 * np.pi, size=N_PARAMS)
    print(f"initial loss={mse_loss(seed):.4f}  acc={accuracy(seed):.2f}")

    result = minimize(
        mse_loss,
        seed,
        method="COBYLA",
        options={"maxiter": 200, "rhobeg": 0.7},
    )
    theta = result.x
    print(f"trained   loss={mse_loss(theta):.4f}  acc={accuracy(theta):.2f}  nfev={result.nfev}")
    print()
    print("x0   x1   score   pred  label")
    for x, y in zip(FEATURES, LABELS):
        score = predict_score(x, theta)
        pred = int(score >= 0.5)
        print(f"{x[0]:.0f}    {x[1]:.0f}    {score:5.3f}    {pred}     {y}")


if __name__ == "__main__":
    main()
