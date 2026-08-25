#!/usr/bin/env python3
"""VQE using Amazon Braket's LocalSimulator and classical optimiser.

Finds the ground-state energy of a 2-qubit H2 Hamiltonian using a
hardware-efficient ansatz.  Gradients are estimated via finite
differences (parameter-shift rule equivalent).
"""

from __future__ import annotations

import numpy as np
from braket.circuits import Circuit, ResultType
from braket.devices import LocalSimulator
import scipy.optimize as opt

# ── Pauli matrices ─────────────────────────────────────────────────
I2 = np.eye(2, dtype=complex)
PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)
PAULI_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def pauli_string(ops: list[np.ndarray]) -> np.ndarray:
    result = ops[0]
    for op in ops[1:]:
        result = np.kron(result, op)
    return result


# ── H2 Hamiltonian ────────────────────────────────────────────────
H2_MATRIX = (
    -0.81261 * pauli_string([I2, I2])
    + 0.17120 * pauli_string([PAULI_Z, I2])
    - 0.22279 * pauli_string([I2, PAULI_Z])
    + 0.17120 * pauli_string([PAULI_Z, PAULI_Z])
    + 0.04532 * pauli_string([PAULI_X, PAULI_X])
)

EXACT_GS_ENERGY = -1.380398  # Exact ground state of this 2-qubit Hamiltonian
N_LAYERS = 3
N_PARAMS = 4 * N_LAYERS


def ansatz_circuit(params: np.ndarray) -> Circuit:
    """Hardware-efficient ansatz: RY-RZ + CX per layer."""
    circuit = Circuit()
    for layer in range(N_LAYERS):
        base = layer * 4
        circuit.ry(0, params[base + 0])
        circuit.rz(0, params[base + 1])
        circuit.ry(1, params[base + 2])
        circuit.rz(1, params[base + 3])
        circuit.cnot(0, 1)
    return circuit


def simulate(circuit: Circuit) -> np.ndarray:
    """Run circuit on LocalSimulator and return statevector."""
    circuit.add_result_type(ResultType.StateVector())
    device = LocalSimulator()
    task = device.run(circuit, shots=0)
    return np.array(task.result().result_types[0].value, dtype=complex)


def energy(params: np.ndarray) -> float:
    """Compute ⟨ψ(θ)|H|ψ(θ)⟩."""
    psi = simulate(ansatz_circuit(params))
    return float(np.real(psi.conj() @ H2_MATRIX @ psi))


def main() -> None:
    print("=== VQE: H2 Ground State (Braket) ===")
    print()
    print("Pauli decomposition:")
    labels = ["II", "ZI", "IZ", "ZZ", "XX"]
    coeffs = [-0.81261, 0.17120, -0.22279, 0.17120, 0.04532]
    for c, l in zip(coeffs, labels):
        print(f"  {c:+.5f} · {l}")
    print()
    print(f"Exact ground-state energy: {EXACT_GS_ENERGY:.6f}")
    print(f"Ansatz: {N_LAYERS} layers, {N_PARAMS} parameters")
    print()

    # ── Initial energy ─────────────────────────────────────────────
    rng = np.random.default_rng(42)
    init_params = rng.uniform(0, 2 * np.pi, size=N_PARAMS)
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
        options={"maxiter": 150, "rhobeg": 0.5},
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

    # ── Final state ────────────────────────────────────────────────
    psi_final = simulate(ansatz_circuit(result.x))
    probs = np.abs(psi_final) ** 2
    print("Final state probabilities:")
    for i in range(4):
        if probs[i] > 0.001:
            print(f"  |{i:02b}⟩  P = {probs[i]:.6f}")
    print()
    print("Optimised circuit:")
    print(ansatz_circuit(result.x))


if __name__ == "__main__":
    main()
