#!/usr/bin/env python3
"""Trotter-Suzuki time evolution of quantum states.

Evolves a state under a ZZ + transverse-field Hamiltonian using
first-order Trotter-Suzuki decomposition, then compares against
exact (matrix-exponential) evolution at several time steps.
"""

from __future__ import annotations

import numpy as np
import qiskit as qk
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector


# ── Hamiltonian: H = J·Z₀Z₁ + h·(X₀ + X₁) ──────────────────────
J = 1.0   # ZZ coupling
H_FIELD = 0.5  # transverse field
HAMILTONIAN = SparsePauliOp.from_list([
    ("ZZ", complex(J)),
    ("XI", complex(H_FIELD)),
    ("IX", complex(H_FIELD)),
])


def exact_evolution_operator(t: float) -> Operator:
    """U(t) = exp(-i H t) via eigendecomposition of the 4×4 matrix."""
    mat = HAMILTONIAN.to_matrix()
    eigenvalues, eigenvectors = np.linalg.eigh(mat)
    exp_diag = np.exp(-1j * eigenvalues * t)
    U = eigenvectors @ np.diag(exp_diag) @ eigenvectors.conj().T
    return Operator(U)


def trotter_step(dt: float) -> Operator:
    """First-order Trotter step: exp(-i Z₀Z₁ dt) · exp(-i h X₀ dt) · exp(-i h X₁ dt)."""
    # ZZ interaction: CNOT-RZ-CNOT
    qc_zz = qk.QuantumCircuit(2)
    qc_zz.cx(0, 1)
    qc_zz.rz(2.0 * J * dt, 1)
    qc_zz.cx(0, 1)

    # Single-qubit X rotations
    qc_x = qk.QuantumCircuit(2)
    qc_x.rx(2.0 * H_FIELD * dt, 0)
    qc_x.rx(2.0 * H_FIELD * dt, 1)

    # Trotter step: U_ZZ · U_X
    step = qc_zz.compose(qc_x)
    return Operator(step)


def trotter_evolution(state: Statevector, t: float, n_steps: int) -> Statevector:
    """Evolve state using n_steps first-order Trotter decomposition."""
    dt = t / n_steps
    U_step = trotter_step(dt)
    evolved = state
    for _ in range(n_steps):
        evolved = evolved.evolve(U_step)
    return evolved


def main() -> None:
    print("=== Time Evolution: ZZ + Transverse Field ===")
    print(f"H = {J:.1f}·Z₀Z₁ + {H_FIELD:.1f}·(X₀ + X₁)")
    print()

    # Initial state: |01⟩ (qubit 0 in |0⟩, qubit 1 in |1⟩)
    init = Statevector.from_int(1, dims=4)  # |01⟩
    probs_init = init.probabilities_dict()
    print(f"Initial state |01⟩ probabilities: {probs_init}")
    print()

    times = [0.5, 1.0, 2.0, 5.0]
    n_trotter_steps = 20

    print(f"{'t':>4s}  {'Method':<10s}  {'|00⟩':>8s}  {'|01⟩':>8s}  {'|10⟩':>8s}  {'|11⟩':>8s}")
    print("-" * 56)

    for t in times:
        # Exact evolution
        U_exact = exact_evolution_operator(t)
        exact_state = init.evolve(U_exact)
        exact_probs = exact_state.probabilities_dict()

        # Trotter evolution
        trotter_state = trotter_evolution(init, t, n_trotter_steps)
        trotter_probs = trotter_state.probabilities_dict()

        def row(label: str, probs: dict) -> str:
            vals = [probs.get(b, 0.0) for b in ("00", "01", "10", "11")]
            return f"  {label:<10s}  {vals[0]:>8.4f}  {vals[1]:>8.4f}  {vals[2]:>8.4f}  {vals[3]:>8.4f}"

        print(f"{t:>4.1f}  {'exact':<10s}  " +
              "  ".join(f"{exact_probs.get(b, 0.0):>8.4f}" for b in ("00", "01", "10", "11")))
        print(f"     {'Trotter':<10s}  " +
              "  ".join(f"{trotter_probs.get(b, 0.0):>8.4f}" for b in ("00", "01", "10", "11")))

        # Fidelity between exact and Trotter
        fidelity = float(np.abs(np.dot(exact_state.data.conj(), trotter_state.data)) ** 2)
        print(f"     Fidelity: {fidelity:.6f}")
        print()

    # ── Convergence: Trotter error vs number of steps ──────────────
    print("=== Trotter Convergence at t = 2.0 ===")
    t_fixed = 2.0
    exact_final = init.evolve(exact_evolution_operator(t_fixed))
    print(f"{'steps':>6s}  {'Fidelity':>10s}  {'Frobenius dist':>14s}")
    print("-" * 34)
    for n_steps in [1, 2, 5, 10, 20, 50]:
        trotter_final = trotter_evolution(init, t_fixed, n_steps)
        fidelity = float(np.abs(np.dot(exact_final.data.conj(), trotter_final.data)) ** 2)
        dist = float(np.linalg.norm(exact_final.data - trotter_final.data))
        print(f"{n_steps:>6d}  {fidelity:>10.6f}  {dist:>14.8f}")

    # ── Show the circuit for a single Trotter step ─────────────────
    print()
    print("=== Single Trotter Step Circuit (dt=0.1) ===")
    step_op = trotter_step(0.1)
    qc_step = qk.QuantumCircuit(2)
    qc_step.append(step_op, [0, 1])
    print(qc_step.draw(output="text"))


if __name__ == "__main__":
    main()
