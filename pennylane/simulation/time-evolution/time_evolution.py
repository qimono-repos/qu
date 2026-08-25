#!/usr/bin/env python3
"""Time evolution using PennyLane's ApproxTimeEvolution.

Evolves a state under a ZZ + transverse field Hamiltonian using
qml.ApproxTimeEvolution (Trotter-Suzuki decomposition) and
compares against exact matrix-exponential evolution at several times.
"""

from __future__ import annotations

import numpy as np
import pennylane as qml

N_QUBITS = 2
dev = qml.device("default.qubit", wires=N_QUBITS)

# ── Hamiltonian: H = J·Z₀Z₁ + h·(X₀ + X₁) ──────────────────────
J, H_FIELD = 1.0, 0.5
HAMILTONIAN = qml.Hamiltonian(
    [J, H_FIELD, H_FIELD],
    [qml.Z(0) @ qml.Z(1), qml.X(0), qml.X(1)],
)


def exact_unitary(t: float) -> np.ndarray:
    """U(t) = exp(-iHt) via eigendecomposition."""
    H_mat = qml.matrix(HAMILTONIAN, wire_order=[0, 1])
    eigenvalues, eigenvectors = np.linalg.eigh(H_mat)
    exp_diag = np.exp(-1j * eigenvalues * t)
    return eigenvectors @ np.diag(exp_diag) @ eigenvectors.conj().T


@qml.qnode(dev)
def trotter_circuit(t: float, n_steps: int, init_state: str = "01") -> qml.QNode:
    """Evolve initial state using ApproxTimeEvolution."""
    if init_state == "11":
        qml.X(wires=0)
        qml.X(wires=1)
    elif init_state == "01":
        qml.X(wires=1)
    elif init_state == "10":
        qml.X(wires=0)
    # |00⟩ needs no preparation
    qml.ApproxTimeEvolution(HAMILTONIAN, t, n_steps)
    return qml.probs(wires=range(N_QUBITS))


def exact_probs(t: float, init_state: str = "01") -> np.ndarray:
    """Compute probabilities via exact matrix exponential."""
    U = exact_unitary(t)

    state_idx = {"00": 0, "01": 1, "10": 2, "11": 3}
    psi0 = np.zeros(4, dtype=complex)
    psi0[state_idx[init_state]] = 1.0

    psi_t = U @ psi0
    return np.abs(psi_t) ** 2


def main() -> None:
    print("=== Time Evolution: ZZ + Transverse Field ===")
    print(f"H = {J:.1f}·Z₀Z₁ + {H_FIELD:.1f}·(X₀ + X₁)")
    print(f"Initial state: |01⟩")
    print()

    times = [0.5, 1.0, 2.0, 5.0]
    n_trotter = 20

    print(f"{'t':>4s}  {'Method':<10s}  {'|00⟩':>8s}  {'|01⟩':>8s}  {'|10⟩':>8s}  {'|11⟩':>8s}")
    print("-" * 56)

    for t in times:
        trotter_probs = trotter_circuit(t, n_trotter)
        exact = exact_probs(t)

        print(f"{t:>4.1f}  {'exact':<10s}  " +
              "  ".join(f"{exact[i]:>8.4f}" for i in range(4)))
        print(f"     {'Trotter':<10s}  " +
              "  ".join(f"{trotter_probs[i]:>8.4f}" for i in range(4)))
        print()

    # ── Trotter convergence ────────────────────────────────────────
    print("=== Trotter Convergence at t = 2.0 ===")
    t_fixed = 2.0
    exact_final = exact_probs(t_fixed)
    print(f"{'steps':>6s}  {'Fidelity':>10s}")
    print("-" * 18)

    U_exact = exact_unitary(t_fixed)
    psi0 = np.zeros(4, dtype=complex)
    psi0[1] = 1.0  # |01⟩
    psi_exact = U_exact @ psi0

    for n_steps in [1, 2, 5, 10, 20, 50]:
        U_approx = qml.matrix(qml.ApproxTimeEvolution(HAMILTONIAN, t_fixed, n_steps), wire_order=[0, 1])
        psi_approx = U_approx @ psi0
        fidelity = float(np.abs(np.dot(psi_exact.conj(), psi_approx)) ** 2)
        print(f"{n_steps:>6d}  {fidelity:>10.6f}")

    print()
    print("=== Trotter Circuit (t=0.5, 4 steps) ===")
    print(qml.draw(trotter_circuit)(0.5, 4))


if __name__ == "__main__":
    main()
