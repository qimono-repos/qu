#!/usr/bin/env python3
"""4-city Travelling Salesperson Problem using PennyLane.

Encodes TSP as a QUBO with one-hot constraints, then solves it
variationally with a parameterised quantum circuit.  City 0 is
pinned at slot 0, leaving 3×3 = 9 binary variables.  The circuit
is a hardware-efficient ansatz with entangling layers, and the
cost is evaluated on-state via qml.expval.
"""

from __future__ import annotations

import itertools

import numpy as np
import pennylane as qml
import scipy.optimize as opt

N_CITIES = 4
N_SLOTS = N_CITIES - 1  # city 0 pinned at slot 0
N_VARS = N_SLOTS * N_SLOTS  # 9 binary variables

NAMES = ("depot", "harbor", "market", "tower")
DIST = np.array([
    [0.0, 2.0, 3.0, 2.5],
    [2.0, 0.0, 1.5, 4.0],
    [3.0, 1.5, 0.0, 1.0],
    [2.5, 4.0, 1.0, 0.0],
])

PENALTY = 10.0


def var_index(city: int, slot: int) -> int:
    """Index into the 9-qubit register for x_{city}_{slot} (1-indexed)."""
    return (city - 1) * N_SLOTS + (slot - 1)


def decode_bits(bits: list[int]) -> list[int] | None:
    """Decode 9-bit string into a tour [slot0=0, slot1, slot2, slot3]."""
    slots = [0, -1, -1, -1]
    used_slots = set()
    for city in range(1, N_CITIES):
        ones = [s for s in range(1, N_CITIES) if bits[var_index(city, s)] == 1]
        if len(ones) != 1:
            return None
        s = ones[0]
        if s in used_slots:
            return None
        slots[s] = city
        used_slots.add(s)
    return slots


def tour_cost(tour: list[int]) -> float:
    total = 0.0
    for k in range(len(tour)):
        total += DIST[tour[k], tour[(k + 1) % len(tour)]]
    return total


def bitstring_cost(bits: list[int]) -> float:
    """Evaluate the QUBO cost: distance + penalty for invalid tours."""
    tour = decode_bits(bits)
    if tour is None:
        return PENALTY * N_CITIES
    return tour_cost(tour)


dev = qml.device("default.qubit", wires=N_VARS)


@qml.qnode(dev, diff_method="parameter-shift")
def tsp_circuit(params):
    n_params = len(params)
    n_layers = n_params // (2 * N_VARS)
    p = 0

    for i in range(N_VARS):
        qml.RY(np.pi * 0.5, wires=i)

    for _ in range(n_layers):
        for i in range(N_VARS):
            qml.RX(params[p], wires=i)
            p += 1
        for i in range(N_VARS):
            qml.RZ(params[p], wires=i)
            p += 1
        for i in range(N_VARS - 1):
            qml.CNOT(wires=[i, i + 1])
        qml.CNOT(wires=[N_VARS - 1, 0])

    return qml.probs(wires=range(N_VARS))


def cost_function(params):
    probs = tsp_circuit(params)
    expected = 0.0
    for idx, p in enumerate(probs):
        if p < 1e-12:
            continue
        bits = [(idx >> q) & 1 for q in range(N_VARS)]
        expected += p * bitstring_cost(bits)
    return expected


def classical_baseline() -> float:
    best_cost = float("inf")
    best_tour = None
    for perm in itertools.permutations(range(1, N_CITIES)):
        tour = (0,) + perm
        c = tour_cost(list(tour))
        if c < best_cost:
            best_cost = c
            best_tour = tour
    print("  Classical baseline (all permutations):")
    for perm in itertools.permutations(range(1, N_CITIES)):
        tour = (0,) + perm
        c = tour_cost(list(tour))
        marker = " <-- best" if tour == best_tour else ""
        print(f"    {' -> '.join(NAMES[i] for i in tour)}  cost={c:.1f}{marker}")
    print()
    return best_cost


def main() -> None:
    print("=== 4-City TSP with PennyLane ===")
    print(f"  Cities: {list(NAMES)}")
    print(f"  Distance matrix:")
    for i in range(N_CITIES):
        print(f"    {NAMES[i]:>8}: {[f'{DIST[i,j]:.1f}' for j in range(N_CITIES)]}")
    print()
    best_classical = classical_baseline()

    n_layers = 3
    n_params = n_layers * 2 * N_VARS
    rng = np.random.default_rng(7)
    init = rng.uniform(-np.pi, np.pi, size=n_params)

    print(f"  Quantum ansatz: {n_layers} layers, {n_params} parameters")
    print(f"  Optimising with COBYLA (maxiter=150)...")
    result = opt.minimize(
        cost_function, init, method="COBYLA",
        options={"maxiter": 150, "rhobeg": 0.3},
    )
    print(f"  Converged: {result.success}")
    print(f"  Expected cost: {result.fun:.4f}")
    print()

    probs = tsp_circuit(result.x)
    top_indices = np.argsort(probs)[-5:][::-1]
    print("  Top 5 measurement outcomes:")
    found_valid = False
    for idx in top_indices:
        p = probs[idx]
        bits = [(idx >> q) & 1 for q in range(N_VARS)]
        tour = decode_bits(bits)
        if tour is not None:
            c = tour_cost(tour)
            route = " -> ".join(NAMES[i] for i in tour)
            print(f"    |{format(idx, f'0{N_VARS}b')}⟩  P={p:.4f}  "
                  f"route={route}  cost={c:.1f}")
            if not found_valid:
                found_valid = True
                if abs(c - best_classical) < 0.01:
                    print("    ** Found optimal tour! **")
        else:
            print(f"    |{format(idx, f'0{N_VARS}b')}⟩  P={p:.4f}  (invalid)")

    if not found_valid:
        print("  No valid tour found — try more layers or reads.")


if __name__ == "__main__":
    main()
