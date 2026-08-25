#!/usr/bin/env python3
"""4-city traveling salesperson as QUBO, solved with simulated annealing.

City 0 is pinned at slot 0.  The remaining 3x3 one-hot matrix gives 9
binary variables.  A large penalty enforces valid tours, and the tour
length is the objective.
"""

from __future__ import annotations

import itertools

import dimod
import matplotlib.pyplot as plt
import neal
import numpy as np

NAMES = ("depot", "harbor", "market", "tower")
DIST = np.array([
    [0.0, 2.0, 3.0, 2.5],
    [2.0, 0.0, 1.5, 4.0],
    [3.0, 1.5, 0.0, 1.0],
    [2.5, 4.0, 1.0, 0.0],
])
N_FREE = 3
N = N_FREE * N_FREE
PENALTY = 8.0


def idx(city: int, slot: int) -> int:
    return (city - 1) * N_FREE + (slot - 1)


def length(order: tuple[int, ...]) -> float:
    return sum(DIST[a, b] for a, b in zip(order, order[1:] + order[:1]))


def decode(bits: str) -> tuple[int, ...] | None:
    flags = [int(b) for b in bits[::-1]]
    slots = [0, -1, -1, -1]
    used_c, used_t = set(), set()
    for city in (1, 2, 3):
        ones = [t for t in (1, 2, 3) if flags[idx(city, t)] == 1]
        if len(ones) != 1:
            return None
        t = ones[0]
        if t in used_t:
            return None
        slots[t] = city
        used_t.add(t)
        used_c.add(city)
    return tuple(slots)


def build_qubo() -> dimod.BinaryQuadraticModel:
    bqm = dimod.BinaryQuadraticModel("BINARY")
    names = [f"x_{c}_{s}" for c in range(1, 4) for s in range(1, 4)]
    for n in names:
        bqm.add_variable(n, 0.0)
    for c in range(1, 4):
        for s1 in range(1, 4):
            for s2 in range(s1 + 1, 4):
                bqm.add_interaction(f"x_{c}_{s1}", f"x_{c}_{s2}", PENALTY)
    for s in range(1, 4):
        for c1 in range(1, 4):
            for c2 in range(c1 + 1, 4):
                bqm.add_interaction(f"x_{c1}_{s}", f"x_{c2}_{s}", PENALTY)
    for c in range(1, 4):
        for s in range(1, 4):
            bqm.add_variable(f"x_{c}_{s}", -PENALTY)
    prev_slot = 0
    for slot in range(1, 4):
        for c_prev in range(1, 4):
            v_prev = f"x_{c_prev}_{prev_slot}" if prev_slot > 0 else None
            for c_next in range(1, 4):
                cost = DIST[c_prev, c_next]
                if v_prev is not None:
                    bqm.add_interaction(v_prev, f"x_{c_next}_{slot}", cost)
                else:
                    bqm.add_variable(f"x_{c_next}_{slot}", cost)
        prev_slot = slot
    last_slot = N_FREE
    for c_last in range(1, 4):
        for c_return in range(1, 4):
            bqm.add_interaction(f"x_{c_last}_{last_slot}", f"x_{c_return}_{1}", DIST[c_last, c_return])
    return bqm


def classical_baseline() -> None:
    best, best_len = None, float("inf")
    for tail in itertools.permutations((1, 2, 3)):
        tour = (0, *tail)
        L = length(tour)
        print(f"  {tour}  {[NAMES[i] for i in tour]}  length={L:.1f}")
        if L < best_len:
            best, best_len = tour, L
    print(f"  Optimal: {best}  {[NAMES[i] for i in best]}  length={best_len:.1f}")
    print()


def visualize_route(tour: tuple[int, ...], total_cost: float) -> None:
    coords = np.array([[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]])
    fig, ax = plt.subplots(figsize=(5, 5))
    for k in range(len(tour)):
        i, j = tour[k], tour[(k + 1) % len(tour)]
        ax.annotate("", xy=coords[j], xytext=coords[i],
                     arrowprops=dict(arrowstyle="-|>", color="C0", lw=2))
    for i in range(4):
        c = "C3" if i == 0 else "C0"
        ax.plot(*coords[i], "o", color=c, markersize=14, zorder=5)
        ax.annotate(NAMES[i], coords[i], textcoords="offset points",
                     xytext=(10, -5), fontsize=11, fontweight="bold")
    ax.set_title(f"TSP  route: {' -> '.join(NAMES[i] for i in tour)}\ntotal length = {total_cost:.1f}")
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(-0.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("tsp_route.png", dpi=150)
    print("Saved tsp_route.png")


def main() -> None:
    print("=== Classical baseline (all permutations) ===")
    classical_baseline()

    print("=== Building QUBO ===")
    bqm = build_qubo()
    print(f"  Variables: {len(bqm.variables)}")
    print(f"  Interactions: {len(bqm.quadratic)}")
    print()

    sampler = neal.SimulatedAnnealingSampler()
    response = sampler.sample(bqm, num_reads=500, num_sweeps=1000)
    sample = response.first.sample
    bits = "".join(str(int(round(sample.get(v, 0)))) for v in bqm.variables)
    tour = decode(bits)

    print("=== Simulated annealing result ===")
    print(f"  Raw bits:    {bits}")
    print(f"  Decoded:     {tour}")
    if tour is not None:
        cost = length(tour)
        print(f"  Route:       {' -> '.join(NAMES[i] for i in tour)}")
        print(f"  Total cost:  {cost:.1f}")
        visualize_route(tour, cost)
    else:
        print("  Invalid tour — increase num_reads or PENALTY")


if __name__ == "__main__":
    main()
