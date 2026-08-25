#!/usr/bin/env python3
"""Construct Hamiltonians with SparsePauliOp and compute expectation values.

Demonstrates how to build molecular and lattice Hamiltonians using
Qiskit's SparsePauliOp, then evaluate expectation values on
Statevector states.  The H2 molecule is represented in a minimal
(2-qubit) basis using pre-computed Pauli coefficients.
"""

from __future__ import annotations

import numpy as np
import qiskit as qk


# ── H2 Hamiltonian (2-qubit BK-Oriol representation) ──────────────
# Coefficients and Pauli strings for H2 at equilibrium bond length
# in the Bravyi-Kitaev / Jordan-Wigner 2-qubit encoding.
# Reference: optimized CI coefficients → Pauli decomposition.
H2_PAULI_SUM = [
    (-0.81261, "II"),
    (0.17120, "IZ"),
    (-0.22279, "ZI"),
    (0.17120, "ZZ"),
    (0.04532, "XX"),
]


def build_pauli_hamiltonian(pauli_terms: list[tuple[float, str]]) -> qk.quantum_info.SparsePauliOp:
    """Build a SparsePauliOp from a list of (coefficient, pauli_string) pairs.

    Qiskit uses little-endian ordering: the rightmost character in the
    Pauli string corresponds to qubit 0.
    """
    coeffs = [complex(c) for c, _ in pauli_terms]
    labels = [label for _, label in pauli_terms]
    return qk.quantum_info.SparsePauliOp.from_list(list(zip(labels, coeffs)))


def expectation_value(state: qk.quantum_info.Statevector, hamiltonian: qk.quantum_info.SparsePauliOp) -> float:
    """Compute <ψ|H|ψ> using Statevector.expectation_value."""
    return float(np.real(state.expectation_value(hamiltonian)))


def main() -> None:
    H = build_pauli_hamiltonian(H2_PAULI_SUM)
    print("=== H2 Hamiltonian (2-qubit representation) ===")
    print()
    print("Pauli decomposition:")
    for coeff, label in zip(H.coeffs, H.paulis.to_labels()):
        print(f"  {coeff.real:+.5f} · {label}")
    print()
    print(f"SparsePauliOp summary: {H.num_qubits} qubits, {len(H)} terms")
    print()

    # ── Matrix representation ──────────────────────────────────────
    mat = H.to_matrix()
    eigenvalues = np.linalg.eigvalsh(mat)
    print(f"Hamiltonian matrix ({mat.shape[0]}×{mat.shape[1]}):")
    print(np.array2string(mat.real, precision=4, suppress_small=True))
    print()
    print(f"Exact eigenvalues: {np.round(eigenvalues, 6)}")
    print(f"Ground state energy: {eigenvalues[0]:.6f}")
    print()

    # ── Expectation values on example states ───────────────────────
    sv_backend = qk.quantum_info.Statevector

    # |00⟩ computational basis
    state_00 = sv_backend.from_int(0, dims=4)
    print(f"<00|H|00> = {expectation_value(state_00, H):.6f}")

    # |11⟩ computational basis
    state_11 = sv_backend.from_int(3, dims=4)
    print(f"<11|H|11> = {expectation_value(state_11, H):.6f}")

    # Uniform superposition |+⟩⊗|+⟩
    plus = sv_backend.from_label("++")
    print(f"<++|H|++> = {expectation_value(plus, H):.6f}")

    # Exact ground state from eigendecomposition
    _, eigvecs = np.linalg.eigh(mat)
    gs_vec = np.ascontiguousarray(eigvecs[:, 0])
    ground = sv_backend(gs_vec)
    print(f"<GS|H|GS> = {expectation_value(ground, H):.6f}  (exact ground state)")
    print()

    # ── Custom ZZ + X lattice Hamiltonian ──────────────────────────
    print("=== Custom 2-qubit ZZ coupling Hamiltonian ===")
    lattice_terms = [
        (1.0, "ZZ"),
        (0.5, "XI"),
        (0.5, "IX"),
    ]
    H_lattice = build_pauli_hamiltonian(lattice_terms)
    print(f"H = {H_lattice}")
    print()
    mat_lattice = H_lattice.to_matrix()
    evals = np.linalg.eigvalsh(mat_lattice)
    print(f"Eigenvalues: {np.round(evals, 6)}")
    print(f"Ground state energy: {evals[0]:.6f}")


if __name__ == "__main__":
    main()
