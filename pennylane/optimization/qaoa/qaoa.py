#!/usr/bin/env python3
"""QAOA for MaxCut on C4 using PennyLane's autograd.

Solves the MaxCut problem on a 4-cycle graph using the Quantum
Approximate Optimization Algorithm.  PennyLane handles automatic
differentiation of the quantum circuit, so the classical optimiser
gradient is computed via parameter-shift rules internally.

Uses qml.ApproxTimeEvolution for compact cost/mixer layers and
qml.expval for the objective.
"""

from __future__ import annotations

import numpy as np
import pennylane as qml
import scipy.optimize as opt

N_QUBITS = 4
LAYERS = 2
EDGES = [(0, 1), (1, 2), (2, 3), (3, 0)]

dev = qml.device("default.qubit", wires=N_QUBITS)


def maxcut_cost_hamiltonian(edges):
    coeffs, ops = [], []
    for i, j in edges:
        coeffs.append(0.5)
        ops.append(qml.Z(i) @ qml.Z(j))
        coeffs.append(-0.5)
        ops.append(qml.Identity(i) @ qml.Identity(j))
    return qml.Hamiltonian(coeffs, ops)


def mixer_hamiltonian(n_qubits):
    return qml.Hamiltonian(
        [1.0] * n_qubits,
        [qml.X(i) for i in range(n_qubits)],
    )


cost_ham = maxcut_cost_hamiltonian(EDGES)
mixer_ham = mixer_hamiltonian(N_QUBITS)


@qml.qnode(dev, diff_method="parameter-shift")
def qaoa_circuit(params):
    p = len(params) // 2
    gammas, betas = params[:p], params[p:]
    qml.Hadamard(wires=range(N_QUBITS))
    for k in range(p):
        qml.ApproxTimeEvolution(cost_ham, gammas[k], 1)
        qml.ApproxTimeEvolution(mixer_ham, betas[k], 1)
    return qml.expval(cost_ham)


def cut_value(bitstring):
    return sum(bitstring[i] != bitstring[j] for i, j in EDGES)


def cost_function(params):
    return -qaoa_circuit(params)


def main() -> None:
    print(f"=== QAOA MaxCut on C{N_QUBITS} ({LAYERS} layers) ===")
    print(f"  Edges: {EDGES}")
    print()

    rng = np.random.default_rng(42)
    init = rng.uniform(0, np.pi, size=2 * LAYERS)
    print(f"  Initial params: {np.round(init, 4)}")
    print()

    result = opt.minimize(
        cost_function, init, method="COBYLA",
        options={"maxiter": 100, "rhobeg": 0.4},
    )

    print("  Optimiser converged:", result.success)
    print(f"  Optimal params: {np.round(result.x, 4)}")
    print(f"  Final cost (neg expval): {result.fun:.6f}")
    print()

    @qml.qnode(dev)
    def probabilities(params):
        p = len(params) // 2
        gammas, betas = params[:p], params[p:]
        qml.Hadamard(wires=range(N_QUBITS))
        for k in range(p):
            qml.ApproxTimeEvolution(cost_ham, gammas[k], 1)
            qml.ApproxTimeEvolution(mixer_ham, betas[k], 1)
        return qml.probs(wires=range(N_QUBITS))

    probs = probabilities(result.x)
    best_idx = np.argmax(probs)
    best_bits = format(best_idx, f"0{N_QUBITS}b")

    print(f"  Most likely: |{best_bits}⟩  cut={cut_value(best_bits)}  "
          f"P={probs[best_idx]:.4f}")
    print()

    top = np.argsort(probs)[-4:][::-1]
    print("  Top 4 outcomes:")
    for idx in top:
        bits = format(idx, f"0{N_QUBITS}b")
        print(f"    |{bits}⟩  cut={cut_value(bits)}  P={probs[idx]:.4f}")

    print()
    print("  Circuit:")
    print(qml.draw(qaoa_circuit)(result.x))


if __name__ == "__main__":
    main()
