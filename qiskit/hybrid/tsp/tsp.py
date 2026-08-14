#!/usr/bin/env python3
"""Traveling salesperson on 4 cities as a one-hot QUBO + a VQE-style loop.

City 0 is fixed at time 0 (the depot). The remaining 3 cities × 3 time
slots are 9 binary variables. The ansatz is a hardware-efficient
RY–CZ ladder, not QAOA, so this file stays independent of hybrid/qaoa.
"""

from __future__ import annotations

import itertools

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from scipy.optimize import minimize


CITIES = ("depot", "harbor", "market", "tower")
N_FREE = 3
N_QUBITS = N_FREE * N_FREE  # 9

# Symmetric distances between the 4 cities (indices 0..3).
DIST = np.array(
    [
        [0.0, 2.0, 3.0, 2.5],
        [2.0, 0.0, 1.5, 4.0],
        [3.0, 1.5, 0.0, 1.0],
        [2.5, 4.0, 1.0, 0.0],
    ],
    dtype=float,
)

PENALTY = 8.0
ANSATZ_LAYERS = 2


def var_index(city: int, slot: int) -> int:
    """Map free city c in {1,2,3} and time slot t in {1,2,3} to a qubit."""
    return (city - 1) * N_FREE + (slot - 1)


def tour_length(order: tuple[int, ...]) -> float:
    """Closed tour length. `order` is a permutation of all 4 city indices."""
    total = 0.0
    for a, b in zip(order, order[1:] + order[:1]):
        total += DIST[a, b]
    return total


def classical_best() -> tuple[tuple[int, ...], float]:
    best: tuple[int, ...] | None = None
    best_len = float("inf")
    for tail in itertools.permutations((1, 2, 3)):
        order = (0, *tail)
        length = tour_length(order)
        if length < best_len:
            best_len = length
            best = order
    assert best is not None
    return best, best_len


def decode_one_hot(bits: str) -> tuple[int, ...] | None:
    """Return a 4-city tour or None if the bitstring is not a valid one-hot."""
    flags = [int(b) for b in bits[::-1]]  # qubit 0 -> index 0
    slots: list[int] = [0, -1, -1, -1]
    used_cities: set[int] = set()
    used_slots: set[int] = set()
    for city in (1, 2, 3):
        ones = [slot for slot in (1, 2, 3) if flags[var_index(city, slot)] == 1]
        if len(ones) != 1:
            return None
        slot = ones[0]
        if slot in used_slots or city in used_cities:
            return None
        slots[slot] = city
        used_slots.add(slot)
        used_cities.add(city)
    if -1 in slots:
        return None
    return tuple(slots)


def qubo_energy(bits: str) -> float:
    """Distance of a valid tour, or a penalty if constraints are broken."""
    tour = decode_one_hot(bits)
    if tour is None:
        return PENALTY
    return tour_length(tour)


def hardware_efficient_ansatz(params: np.ndarray) -> QuantumCircuit:
    thetas = params.reshape(ANSATZ_LAYERS + 1, N_QUBITS)
    qc = QuantumCircuit(N_QUBITS, name="tsp_ansatz")
    for layer in range(ANSATZ_LAYERS):
        for q in range(N_QUBITS):
            qc.ry(float(thetas[layer, q]), q)
        for q in range(N_QUBITS - 1):
            qc.cz(q, q + 1)
    for q in range(N_QUBITS):
        qc.ry(float(thetas[ANSATZ_LAYERS, q]), q)
    return qc


def expected_energy(params: np.ndarray) -> float:
    sv = Statevector.from_instruction(hardware_efficient_ansatz(params))
    return float(
        sum(prob * qubo_energy(bits) for bits, prob in sv.probabilities_dict().items())
    )


def most_likely_tour(params: np.ndarray) -> tuple[str, float, tuple[int, ...] | None, float]:
    probs = Statevector.from_instruction(hardware_efficient_ansatz(params)).probabilities_dict()
    bits, prob = max(probs.items(), key=lambda kv: kv[1])
    tour = decode_one_hot(bits)
    length = tour_length(tour) if tour is not None else float("nan")
    return bits, float(prob), tour, length


def main() -> None:
    opt_tour, opt_len = classical_best()
    print("4-city TSP  (depot fixed at t=0, return to depot)")
    print("cities:", ", ".join(f"{i}:{name}" for i, name in enumerate(CITIES)))
    print("distance matrix:")
    print(DIST)
    print(f"classical optimum: {opt_tour}  length={opt_len:.2f}")
    print(f"names: {' -> '.join(CITIES[i] for i in opt_tour)} -> {CITIES[0]}\n")

    rng = np.random.default_rng(21)
    n_params = (ANSATZ_LAYERS + 1) * N_QUBITS
    seed = rng.normal(0.0, 0.4, size=n_params)

    result = minimize(
        expected_energy,
        seed,
        method="COBYLA",
        options={"maxiter": 60, "rhobeg": 0.5},
    )

    bits, prob, tour, length = most_likely_tour(result.x)
    print(f"VQE-style hybrid loop  success={result.success}  nfev={result.nfev}")
    print(f"expected QUBO energy: {result.fun:.3f}")
    print(f"most likely bitstring |{bits}>   P={prob:.3f}")
    if tour is None:
        print("that bitstring is not a valid one-hot tour (constraints not met)")
    else:
        names = " -> ".join(CITIES[i] for i in tour)
        print(f"decoded tour: {tour}   {names} -> {CITIES[0]}   length={length:.2f}")


if __name__ == "__main__":
    main()
