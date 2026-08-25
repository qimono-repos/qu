#!/usr/bin/env python3
"""VQE for the H2 ground state using PennyLane.

Uses a hardware-efficient ansatz with parameter-shift gradients
and COBYLA optimisation to find the ground-state energy of a
2-qubit H2 Hamiltonian.
"""

from __future__ import annotations

import numpy as np
import pennylane as qml
import scipy.optimize as opt

N_QUBITS = 2
N_LAYERS = 3
dev = qml.device("default.qubit", wires=N_QUBITS)

# ── H2 Hamiltonian (2-qubit Jordan-Wigner) ────────────────────────
H2_HAMILTONIAN = qml.Hamiltonian(
    [-0.81261, 0.17120, -0.22279, 0.17120, 0.04532],
    [
        qml.Identity(0),
        qml.Z(0),
        qml.Z(1),
        qml.Z(0) @ qml.Z(1),
        qml.X(0) @ qml.X(1),
    ],
)

EXACT_GS_ENERGY = -1.380398  # Exact ground state of this 2-qubit Hamiltonian


# ── Ansatz ─────────────────────────────────────────────────────────
@qml.qnode(dev, diff_method="parameter-shift")
def ansatz(params):
    """Hardware-efficient ansatz: RY-RZ + CX per layer."""
    for layer in range(N_LAYERS):
        base = layer * 4
        qml.RY(params[base + 0], wires=0)
        qml.RZ(params[base + 1], wires=0)
        qml.RY(params[base + 2], wires=1)
        qml.RZ(params[base + 3], wires=1)
        qml.CNOT(wires=[0, 1])
    return qml.expval(H2_HAMILTONIAN)


def energy(params):
    return float(ansatz(params))


def main() -> None:
    print("=== VQE: H2 Ground State (PennyLane) ===")
    print()
    print("Hamiltonian (Pauli decomposition):")
    for coeff, op in zip(H2_HAMILTONIAN.coeffs, H2_HAMILTONIAN.ops):
        print(f"  {float(coeff):+.5f} · {op.name if hasattr(op, 'name') else op}")
    print()
    print(f"Exact ground-state energy: {EXACT_GS_ENERGY:.6f}")
    print(f"Ansatz: {N_LAYERS} layers, {4 * N_LAYERS} parameters")
    print()

    # ── Initial energy ─────────────────────────────────────────────
    rng = np.random.default_rng(42)
    init_params = rng.uniform(0, 2 * np.pi, size=4 * N_LAYERS)
    print(f"Initial energy: {energy(init_params):.6f}")
    print()

    # ── Optimisation with COBYLA ───────────────────────────────────
    history: list[float] = []

    def callback(xk) -> None:
        history.append(energy(xk))

    result = opt.minimize(
        energy,
        init_params,
        method="COBYLA",
        options={"maxiter": 200, "rhobeg": 0.5},
        callback=callback,
    )

    print(f"Optimiser: COBYLA  success={result.success}  nfev={result.nfev}")
    print(f"Optimised energy: {result.fun:.6f}")
    print(f"Error vs exact:   {abs(result.fun - EXACT_GS_ENERGY):.6f}")
    print()

    # ── Energy convergence ─────────────────────────────────────────
    print("Energy convergence (sampled every N iterations):")
    step = max(1, len(history) // 10)
    for i in range(0, len(history), step):
        print(f"  iter {i + 1:>3d}  energy = {history[i]:.6f}")
    if (len(history) - 1) % step != 0:
        print(f"  iter {len(history):>3d}  energy = {history[-1]:.6f}")
    print()

    # ── Final state probabilities ──────────────────────────────────
    probs = qml.probs(wires=range(N_QUBITS))
    final_probs = ansatz(result.x)
    # Re-run to get probs instead of expval
    @qml.qnode(dev)
    def final_circuit(params):
        for layer in range(N_LAYERS):
            base = layer * 4
            qml.RY(params[base + 0], wires=0)
            qml.RZ(params[base + 1], wires=0)
            qml.RY(params[base + 2], wires=1)
            qml.RZ(params[base + 3], wires=1)
            qml.CNOT(wires=[0, 1])
        return qml.probs(wires=range(N_QUBITS))

    state_probs = final_circuit(result.x)
    print("Final state probabilities:")
    for i, p in enumerate(state_probs):
        if p > 0.001:
            print(f"  |{i:02b}⟩  P = {p:.6f}")
    print()
    print("Optimised circuit:")
    print(qml.draw(final_circuit)(result.x))


if __name__ == "__main__":
    main()
