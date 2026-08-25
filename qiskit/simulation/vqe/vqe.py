#!/usr/bin/env python3
"""Variational Quantum Eigensolver for the H2 ground state.

Uses a hardware-efficient ansatz with COBYLA optimisation to find the
ground-state energy of a 2-qubit H2 Hamiltonian.  All expectation values
are computed exactly via Statevector (no shots / sampling noise).
"""

from __future__ import annotations

import numpy as np
import qiskit as qk
import scipy.optimize as opt


# ── H2 Hamiltonian (2-qubit Jordan-Wigner) ────────────────────────
H2_PAULIS = [
    (-0.81261, "II"),
    (0.17120, "IZ"),
    (-0.22279, "ZI"),
    (0.17120, "ZZ"),
    (0.04532, "XX"),
]

HAMILTONIAN = qk.quantum_info.SparsePauliOp.from_list(
    [(label, complex(coeff)) for coeff, label in H2_PAULIS]
)

# Exact ground-state energy for reference
EXACT_GS_ENERGY = -1.380398  # Exact ground state of this 2-qubit Hamiltonian


# ── Parameterised ansatz ───────────────────────────────────────────
def ansatz_circuit(params: np.ndarray) -> qk.QuantumCircuit:
    """Hardware-efficient ansatz: RY-RZ layers + entangling CX gates.

    Structure per layer:
      RY(θ₀) RZ(θ₁) on qubit 0
      RY(θ₂) RZ(θ₃) on qubit 1
      CX(0→1)
    """
    n_layers = len(params) // 4
    qc = qk.QuantumCircuit(2)
    for layer in range(n_layers):
        base = layer * 4
        qc.ry(params[base + 0], 0)
        qc.rz(params[base + 1], 0)
        qc.ry(params[base + 2], 1)
        qc.rz(params[base + 3], 1)
        qc.cx(0, 1)
    return qc


def energy(params: np.ndarray) -> float:
    """Compute ⟨ψ(θ)|H|ψ(θ)⟩ using Statevector."""
    qc = ansatz_circuit(params)
    sv = qk.quantum_info.Statevector.from_instruction(qc)
    return float(np.real(sv.expectation_value(HAMILTONIAN)))


def main() -> None:
    print("=== VQE: H2 Ground State (2-qubit) ===")
    print()
    print("Hamiltonian (Pauli decomposition):")
    for coeff, label in H2_PAULIS:
        print(f"  {coeff:+.5f} · {label}")
    print()
    print(f"Exact ground-state energy: {EXACT_GS_ENERGY:.6f}")
    print()

    n_layers = 3
    n_params = 4 * n_layers  # 12 parameters
    print(f"Ansatz: {n_layers} layers, {n_params} parameters")
    print()

    # ── Optimisation with COBYLA ───────────────────────────────────
    rng = np.random.default_rng(42)
    init_params = rng.uniform(0, 2 * np.pi, size=n_params)

    history: list[tuple[int, float]] = []

    def callback(xk) -> None:
        e = energy(xk)
        history.append((len(history) + 1, e))

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
    for i, (iter_num, e) in enumerate(history[::step]):
        print(f"  iter {iter_num:>3d}  energy = {e:.6f}")
    # Always show the final point
    if history[-1][0] % step != 0:
        i, e = history[-1]
        print(f"  iter {i:>3d}  energy = {e:.6f}")
    print()

    # ── Final circuit and state ────────────────────────────────────
    qc_optimised = ansatz_circuit(result.x)
    sv = qk.quantum_info.Statevector.from_instruction(qc_optimised)
    probs = sv.probabilities_dict()

    print("Final state probabilities:")
    for bitstring in sorted(probs.keys()):
        if probs[bitstring] > 0.001:
            print(f"  |{bitstring}⟩  P = {probs[bitstring]:.6f}")
    print()
    print("Optimised circuit:")
    print(qc_optimised.draw(output="text"))


if __name__ == "__main__":
    main()
