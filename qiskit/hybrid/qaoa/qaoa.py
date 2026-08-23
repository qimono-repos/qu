#!/usr/bin/env python3
"""QAOA for MaxCut on a 4-vertex cycle, written as a hybrid loop.

The cost Hamiltonian, mixer, expectation-value estimator, and COBYLA
outer loop are all local to this file. The traveling-salesperson and
QML examples use different graphs, encodings, and ansatze on purpose.
"""

from __future__ import annotations

import math

import numpy as np
import qiskit as qk
from scipy.optimize import minimize


# Cycle graph C4: vertices 0-1-2-3-0.
EDGES: tuple[tuple[int, int], ...] = ((0, 1), (1, 2), (2, 3), (3, 0))
N_QUBITS = 4
LAYERS = 2


def maxcut_value(bitstring: str, edges: tuple[tuple[int, int], ...]) -> int:
    """Number of cut edges. bitstring is Qiskit order (qubit 0 on the right)."""
    bits = bitstring[::-1]
    return sum(bits[i] != bits[j] for i, j in edges)


def cost_layer(gamma: float, edges: tuple[tuple[int, int], ...]) -> qk.QuantumCircuit:
    """exp(-i gamma sum_{(i,j) in E} Z_i Z_j) via CNOT-RZ-CNOT."""
    layer = qk.QuantumCircuit(N_QUBITS, name="cost")
    for i, j in edges:
        layer.cx(i, j)
        layer.rz(2.0 * gamma, j)
        layer.cx(i, j)
    return layer


def mixer_layer(beta: float) -> qk.QuantumCircuit:
    """exp(-i beta sum_i X_i)."""
    layer = qk.QuantumCircuit(N_QUBITS, name="mixer")
    for q in range(N_QUBITS):
        layer.rx(2.0 * beta, q)
    return layer


def qaoa_circuit(params: np.ndarray, edges: tuple[tuple[int, int], ...], p: int) -> qk.QuantumCircuit:
    gammas = params[:p]
    betas = params[p:]
    qc = qk.QuantumCircuit(N_QUBITS, name="qaoa")
    qc.h(range(N_QUBITS))
    for k in range(p):
        qc.compose(cost_layer(float(gammas[k]), edges), inplace=True)
        qc.compose(mixer_layer(float(betas[k])), inplace=True)
    return qc


def expected_cut(params: np.ndarray, edges: tuple[tuple[int, int], ...], p: int) -> float:
    sv = qk.quantum_info.Statevector.from_instruction(qaoa_circuit(params, edges, p))
    probs = sv.probabilities_dict()
    return sum(prob * maxcut_value(bits, edges) for bits, prob in probs.items())


def energy_to_minimize(params: np.ndarray, edges: tuple[tuple[int, int], ...], p: int) -> float:
    # MaxCut maximises the cut, so the classical optimiser minimises the negation.
    return -expected_cut(params, edges, p)


def decode_best(params: np.ndarray, edges: tuple[tuple[int, int], ...], p: int) -> tuple[str, int, float]:
    sv = qk.quantum_info.Statevector.from_instruction(qaoa_circuit(params, edges, p))
    probs = sv.probabilities_dict()
    best_bits, best_p = max(probs.items(), key=lambda kv: kv[1])
    return best_bits, maxcut_value(best_bits, edges), float(best_p)


def main() -> None:
    print(f"QAOA MaxCut on C{N_QUBITS}, p={LAYERS} layers")
    print(f"edges: {EDGES}")
    print("optimal cut size on a 4-cycle is 4 (any balanced 2-2 colouring)\n")

    rng = np.random.default_rng(7)
    seed = rng.uniform(0.0, math.pi, size=2 * LAYERS)

    history: list[float] = []

    def cb(intermediate_result) -> None:
        cut = -float(intermediate_result.fun)
        history.append(cut)

    result = minimize(
        energy_to_minimize,
        seed,
        args=(EDGES, LAYERS),
        method="COBYLA",
        options={"maxiter": 80, "rhobeg": 0.4},
        callback=cb,
    )

    bits, cut, prob = decode_best(result.x, EDGES, LAYERS)
    assignment = bits[::-1]
    print(f"optimiser success={result.success}  nfev={result.nfev}")
    print(f"expected cut after training: {expected_cut(result.x, EDGES, LAYERS):.3f}")
    print(f"most likely bitstring |{bits}>  (qubit 0 on the right)")
    print(f"colouring of vertices 0..3: {assignment}   cut={cut}   P={prob:.3f}")
    if history:
        print(f"expected-cut trajectory: {[round(v, 3) for v in history[:: max(1, len(history)//8)]]}")


if __name__ == "__main__":
    main()
