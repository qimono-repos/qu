#!/usr/bin/env python3
"""Trotter time evolution using Amazon Braket circuits.

Evolves a state under a ZZ + transverse field Hamiltonian using
first-order Trotter decomposition built from Braket gates, then
compares against exact (matrix-exponential) evolution.
"""

from __future__ import annotations

import numpy as np
from braket.circuits import Circuit, ResultType
from braket.devices import LocalSimulator

# ── Pauli matrices ─────────────────────────────────────────────────
I2 = np.eye(2, dtype=complex)
PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)
PAULI_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def pauli_string(ops: list[np.ndarray]) -> np.ndarray:
    result = ops[0]
    for op in ops[1:]:
        result = np.kron(result, op)
    return result


# ── Hamiltonian: H = J·Z₀Z₁ + h·(X₀ + X₁) ──────────────────────
J, H_FIELD = 1.0, 0.5
H_MATRIX = (
    J * pauli_string([PAULI_Z, PAULI_Z])
    + H_FIELD * pauli_string([PAULI_X, I2])
    + H_FIELD * pauli_string([I2, PAULI_X])
)


def exact_unitary(t: float) -> np.ndarray:
    """U(t) = exp(-iHt) via eigendecomposition."""
    eigenvalues, eigenvectors = np.linalg.eigh(H_MATRIX)
    exp_diag = np.exp(-1j * eigenvalues * t)
    return eigenvectors @ np.diag(exp_diag) @ eigenvectors.conj().T


def trotter_circuit(t: float, n_steps: int) -> Circuit:
    """Build first-order Trotter circuit for evolution time t."""
    dt = t / n_steps
    circuit = Circuit()

    # Initial state: |01⟩
    circuit.x(1)

    for _ in range(n_steps):
        # ZZ interaction: CNOT(0→1) - RZ(2Jdt) on qubit 1 - CNOT(0→1)
        circuit.cnot(0, 1)
        circuit.rz(1, 2.0 * J * dt)
        circuit.cnot(0, 1)

        # Transverse field: RX(2hdt) on each qubit
        circuit.rx(0, 2.0 * H_FIELD * dt)
        circuit.rx(1, 2.0 * H_FIELD * dt)

    return circuit


def simulate(circuit: Circuit) -> np.ndarray:
    """Run circuit on LocalSimulator and return statevector."""
    circuit.add_result_type(ResultType.StateVector())
    device = LocalSimulator()
    task = device.run(circuit, shots=0)
    return np.array(task.result().result_types[0].value, dtype=complex)


def statevector_from_index(idx: int, n_qubits: int = 2) -> np.ndarray:
    """Computational basis state |idx⟩ as a vector."""
    psi = np.zeros(2**n_qubits, dtype=complex)
    psi[idx] = 1.0
    return psi


def main() -> None:
    print("=== Time Evolution: ZZ + Transverse Field ===")
    print(f"H = {J:.1f}·Z₀Z₁ + {H_FIELD:.1f}·(X₀ + X₁)")
    print(f"Initial state: |01⟩")
    print()

    times = [0.5, 1.0, 2.0, 5.0]
    n_trotter = 20

    psi0 = statevector_from_index(1)  # |01⟩

    print(f"{'t':>4s}  {'Method':<10s}  {'|00⟩':>8s}  {'|01⟩':>8s}  {'|10⟩':>8s}  {'|11⟩':>8s}")
    print("-" * 56)

    for t in times:
        # Exact evolution
        U_exact = exact_unitary(t)
        psi_exact = U_exact @ psi0
        exact_probs = np.abs(psi_exact) ** 2

        # Trotter evolution
        circuit = trotter_circuit(t, n_trotter)
        psi_trotter = simulate(circuit)
        trotter_probs = np.abs(psi_trotter) ** 2

        print(f"{t:>4.1f}  {'exact':<10s}  " +
              "  ".join(f"{exact_probs[i]:>8.4f}" for i in range(4)))
        print(f"     {'Trotter':<10s}  " +
              "  ".join(f"{trotter_probs[i]:>8.4f}" for i in range(4)))

        fidelity = float(np.abs(np.dot(psi_exact.conj(), psi_trotter)) ** 2)
        print(f"     Fidelity: {fidelity:.6f}")
        print()

    # ── Trotter convergence ────────────────────────────────────────
    print("=== Trotter Convergence at t = 2.0 ===")
    t_fixed = 2.0
    U_exact = exact_unitary(t_fixed)
    psi_exact_final = U_exact @ psi0

    print(f"{'steps':>6s}  {'Fidelity':>10s}  {'Frobenius dist':>14s}")
    print("-" * 34)
    for n_steps in [1, 2, 5, 10, 20, 50]:
        circuit = trotter_circuit(t_fixed, n_steps)
        psi_approx = simulate(circuit)
        fidelity = float(np.abs(np.dot(psi_exact_final.conj(), psi_approx)) ** 2)
        dist = float(np.linalg.norm(psi_exact_final - psi_approx))
        print(f"{n_steps:>6d}  {fidelity:>10.6f}  {dist:>14.8f}")

    # ── Show single Trotter step circuit ───────────────────────────
    print()
    print("=== Single Trotter Step Circuit (dt=0.1) ===")
    dt = 0.1
    step_circuit = Circuit()
    step_circuit.cnot(0, 1)
    step_circuit.rz(1, 2.0 * J * dt)
    step_circuit.cnot(0, 1)
    step_circuit.rx(0, 2.0 * H_FIELD * dt)
    step_circuit.rx(1, 2.0 * H_FIELD * dt)
    print(step_circuit)


if __name__ == "__main__":
    main()
