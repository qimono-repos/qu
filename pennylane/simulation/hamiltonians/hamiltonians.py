#!/usr/bin/env python3
"""Construct Hamiltonians with PennyLane and compute expectation values.

Demonstrates building molecular and lattice Hamiltonians using
qml.Hamiltonian, then evaluating expectation values on quantum
circuits executed on the default.qubit simulator.
"""

from __future__ import annotations

import pennylane as qml
import numpy as np

N_QUBITS = 2
dev = qml.device("default.qubit", wires=N_QUBITS)


# ── H2 Hamiltonian (2-qubit representation) ───────────────────────
H2_TERMS = [
    (-0.81261, qml.Identity(0)),
    (0.17120, qml.Z(0)),
    (-0.22279, qml.Z(1)),
    (0.17120, qml.Z(0) @ qml.Z(1)),
    (0.04532, qml.X(0) @ qml.X(1)),
]

H2_HAMILTONIAN = qml.Hamiltonian([c for c, _ in H2_TERMS], [op for _, op in H2_TERMS])

# ── ZZ + transverse field lattice Hamiltonian ─────────────────────
J, H_FIELD = 1.0, 0.5
LATTICE_HAMILTONIAN = qml.Hamiltonian(
    [J, H_FIELD, H_FIELD],
    [qml.Z(0) @ qml.Z(1), qml.X(0), qml.X(1)],
)


def main() -> None:
    print("=== H2 Hamiltonian (PennyLane) ===")
    print()
    print("Pauli decomposition:")
    for coeff, op in zip(H2_HAMILTONIAN.coeffs, H2_HAMILTONIAN.ops):
        print(f"  {float(coeff):+.5f} · {op.name if hasattr(op, 'name') else op}")
    print()

    # ── Expectation values on example states ───────────────────────
    @qml.qnode(dev)
    def expval_circuit(state_prep):
        state_prep()
        return qml.expval(H2_HAMILTONIAN)

    @qml.qnode(dev)
    def probs_circuit(state_prep):
        state_prep()
        return qml.probs(wires=range(N_QUBITS))

    # |00⟩
    e00 = qml.QNode(lambda: qml.expval(H2_HAMILTONIAN), dev)()
    print(f"<00|H|00> = {e00:.6f}")

    # |+⟩|+⟩ via Hadamards
    @qml.qnode(dev)
    def plus_plus():
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)
        return qml.expval(H2_HAMILTONIAN)

    epp = plus_plus()
    print(f"<++|H|++> = {epp:.6f}")

    # |11⟩ via X gates
    @qml.qnode(dev)
    def state_11():
        qml.X(wires=0)
        qml.X(wires=1)
        return qml.expval(H2_HAMILTONIAN)

    e11 = state_11()
    print(f"<11|H|11> = {e11:.6f}")
    print()

    # ── Exact ground state via matrix ──────────────────────────────
    H_mat = qml.matrix(H2_HAMILTONIAN, wire_order=[0, 1])
    eigenvalues = np.linalg.eigvalsh(H_mat)
    print(f"Exact eigenvalues: {np.round(eigenvalues, 6)}")
    print(f"Ground state energy: {eigenvalues[0]:.6f}")
    print()

    # ── Lattice Hamiltonian ────────────────────────────────────────
    print("=== ZZ + Transverse Field Lattice Hamiltonian ===")
    print(f"H = {J:.1f}·Z₀Z₁ + {H_FIELD:.1f}·(X₀ + X₁)")
    print()

    @qml.qnode(dev)
    def lattice_expval(state_prep):
        state_prep()
        return qml.expval(LATTICE_HAMILTONIAN)

    def prep_01():
        qml.X(wires=1)

    e_lattice = lattice_expval(prep_01)
    print(f"<01|H|01> = {e_lattice:.6f}")

    @qml.qnode(dev)
    def lattice_uniform():
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)
        return qml.expval(LATTICE_HAMILTONIAN)

    e_uniform = lattice_uniform()
    print(f"<++|H|++> = {e_uniform:.6f}")

    H_lattice_mat = qml.matrix(LATTICE_HAMILTONIAN, wire_order=[0, 1])
    evals = np.linalg.eigvalsh(H_lattice_mat)
    print(f"Exact eigenvalues: {np.round(evals, 6)}")
    print(f"Ground state energy: {evals[0]:.6f}")

    print()
    print("Circuit drawing (lattice expval on |01⟩):")
    print(qml.draw(lattice_expval)(prep_01))


if __name__ == "__main__":
    main()
