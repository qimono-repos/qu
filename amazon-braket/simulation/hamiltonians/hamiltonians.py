#!/usr/bin/env python3
"""Hamiltonian construction and expectation values using Amazon Braket.

Demonstrates how to build Pauli Hamiltonians as matrices and compute
expectation values on quantum circuits simulated with LocalSimulator.
The H2 molecule Hamiltonian and a custom ZZ lattice model are shown.
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
    """Kronecker product of a list of 2×2 Pauli matrices."""
    result = ops[0]
    for op in ops[1:]:
        result = np.kron(result, op)
    return result


# ── H2 Hamiltonian (2-qubit) ─────────────────────────────────────
H2_PAULIS = [
    (-0.81261, [I2, I2]),
    (0.17120, [PAULI_Z, I2]),
    (-0.22279, [I2, PAULI_Z]),
    (0.17120, [PAULI_Z, PAULI_Z]),
    (0.04532, [PAULI_X, PAULI_X]),
]

H2_MATRIX = sum(coeff * pauli_string(ops) for coeff, ops in H2_PAULIS)

# ── Lattice Hamiltonian: H = J·Z₀Z₁ + h·(X₀ + X₁) ──────────────
J, H_FIELD = 1.0, 0.5
LATTICE_MATRIX = (
    J * pauli_string([PAULI_Z, PAULI_Z])
    + H_FIELD * pauli_string([PAULI_X, I2])
    + H_FIELD * pauli_string([I2, PAULI_X])
)


def statevector_from_circuit(circuit: Circuit) -> np.ndarray:
    """Simulate circuit and return the statevector.

    Braket's default simulator returns a full 2^n statevector only
    when every qubit has at least one gate.  We add identity gates on
    all qubits to guarantee the full statevector is returned.
    """
    n_qubits = max(circuit.qubit_count, 2)
    for q in range(n_qubits):
        circuit.i(q)
    circuit.add_result_type(ResultType.StateVector())
    device = LocalSimulator()
    task = device.run(circuit, shots=0)
    return np.array(task.result().result_types[0].value, dtype=complex)


def expval_from_circuit(circuit: Circuit, hamiltonian: np.ndarray) -> float:
    """Compute ⟨ψ|H|ψ> from a circuit's output statevector."""
    psi = statevector_from_circuit(circuit)
    return float(np.real(psi.conj() @ hamiltonian @ psi))


def basis_state(idx: int, n_qubits: int = 2) -> np.ndarray:
    """Computational basis state |idx⟩ as a vector."""
    psi = np.zeros(2**n_qubits, dtype=complex)
    psi[idx] = 1.0
    return psi


def expval_basis(idx: int, hamiltonian: np.ndarray) -> float:
    """⟨idx|H|idx⟩ via direct matrix multiplication."""
    psi = basis_state(idx)
    return float(np.real(psi.conj() @ hamiltonian @ psi))


def main() -> None:
    print("=== H2 Hamiltonian (Braket) ===")
    print()
    print("Pauli decomposition:")
    labels = ["II", "ZI", "IZ", "ZZ", "XX"]
    for (coeff, _), label in zip(H2_PAULIS, labels):
        print(f"  {coeff:+.5f} · {label}")
    print()
    print(f"Hamiltonian matrix ({H2_MATRIX.shape[0]}×{H2_MATRIX.shape[1]}):")
    print(np.array2string(H2_MATRIX.real, precision=4, suppress_small=True))
    print()

    eigenvalues = np.linalg.eigvalsh(H2_MATRIX)
    print(f"Exact eigenvalues: {np.round(eigenvalues, 6)}")
    print(f"Ground state energy: {eigenvalues[0]:.6f}")
    print()

    # ── Expectation values on example states ───────────────────────
    def circuit_11() -> Circuit:
        c = Circuit()
        c.x(0)
        c.x(1)
        return c

    def circuit_plusplus() -> Circuit:
        c = Circuit()
        c.h(0)
        c.h(1)
        return c

    print("Expectation values:")
    print(f"  <00|H|00> = {expval_basis(0, H2_MATRIX):.6f}")
    print(f"  <11|H|11> = {expval_basis(3, H2_MATRIX):.6f}")
    print(f"  <++|H|++> = {expval_from_circuit(circuit_plusplus(), H2_MATRIX):.6f}")

    # Exact ground state
    _, eigvecs = np.linalg.eigh(H2_MATRIX)
    psi_gs = np.ascontiguousarray(eigvecs[:, 0])
    print(f"  <GS|H|GS> = {float(np.real(psi_gs.conj() @ H2_MATRIX @ psi_gs)):.6f}  (exact)")
    print()

    # ── Lattice Hamiltonian ────────────────────────────────────────
    print("=== ZZ + Transverse Field Lattice Hamiltonian ===")
    print(f"H = {J:.1f}·Z₀Z₁ + {H_FIELD:.1f}·(X₀ + X₁)")
    print()

    evals = np.linalg.eigvalsh(LATTICE_MATRIX)
    print(f"Exact eigenvalues: {np.round(evals, 6)}")
    print(f"Ground state energy: {evals[0]:.6f}")
    print()

    print(f"  <01|H|01> = {expval_basis(1, LATTICE_MATRIX):.6f}")
    print(f"  <++|H|++> = {expval_from_circuit(circuit_plusplus(), LATTICE_MATRIX):.6f}")

    # ── Statevector inspection ─────────────────────────────────────
    print()
    print("=== Statevector Output ===")
    sv = statevector_from_circuit(circuit_plusplus())
    print(f"|++⟩ statevector: {sv}")
    probs = np.abs(sv) ** 2
    print(f"Probabilities: |00⟩={probs[0]:.4f}  |01⟩={probs[1]:.4f}  "
          f"|10⟩={probs[2]:.4f}  |11⟩={probs[3]:.4f}")


if __name__ == "__main__":
    main()
