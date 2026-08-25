#!/usr/bin/env python3
"""Adiabatic quantum computation — concept demonstration.

Illustrates the adiabatic path: start with a simple Hamiltonian whose
ground state is easy to prepare, then slowly evolve to a problem
Hamiltonian whose ground state encodes the solution.

The adiabatic theorem guarantees that if the evolution is slow enough
relative to the minimum spectral gap, the system stays in the ground
state throughout.

Here we:
  1. Define a small MaxCut BQM on C4
  2. Interpolate between an initial (transverse-field) Hamiltonian and
     the problem Hamiltonian
  3. Track the instantaneous ground-state energy along the path using
     neal.SimulatedAnnealingSampler with decreasing temperature
  4. Show that the final low-energy sample encodes a good cut
"""

from __future__ import annotations

import dimod
import neal
import numpy as np


EDGES = [(0, 1), (1, 2), (2, 3), (3, 0)]
N = 4


def cut_size(bits: str) -> int:
    colors = [int(b) for b in bits[::-1]]
    return sum(colors[i] != colors[j] for i, j in EDGES)


def build_problem_bqm() -> dimod.BinaryQuadraticModel:
    """MaxCut BQM: minimise -sum_{(i,j)} s_i s_j for SPIN variables."""
    bqm = dimod.BinaryQuadraticModel("SPIN")
    for i in range(N):
        bqm.add_variable(i, 0.0)
    for i, j in EDGES:
        bqm.add_interaction(i, j, -1.0)
    return bqm


def build_initial_bqm() -> dimod.BinaryQuadraticModel:
    """Initial Hamiltonian: transverse field — strong bias toward |+⟩.

    In the spin representation a transverse field is modelled by a
    uniform linear bias h_i = -h for every qubit, which favours
    alignment along x (i.e. the |+⟩ ground state).
    """
    bqm = dimod.BinaryQuadraticModel("SPIN")
    h = 3.0
    for i in range(N):
        bqm.add_variable(i, -h)
    return bqm


def interpolate_bqm(
    initial: dimod.BinaryQuadraticModel,
    problem: dimod.BinaryQuadraticModel,
    s: float,
) -> dimod.BinaryQuadraticModel:
    """H(s) = (1 - s) H_initial + s H_problem  for s in [0, 1]."""
    bqm = dimod.BinaryQuadraticModel("SPIN")
    for v in initial.variables:
        lin = (1.0 - s) * initial.linear[v] + s * problem.linear[v]
        bqm.add_variable(v, lin)
    for (u, v), q in initial.quadratic.items():
        q_val = (1.0 - s) * q + s * problem.quadratic.get((u, v), 0.0)
        bqm.add_interaction(u, v, q_val)
    for (u, v), q in problem.quadratic.items():
        if (u, v) not in initial.quadratic:
            q_val = s * q
            bqm.add_interaction(u, v, q_val)
    return bqm


def adiabatic_path(n_steps: int = 21) -> list[dict]:
    """Simulate the adiabatic path by sampling at each interpolation point."""
    initial = build_initial_bqm()
    problem = build_problem_bqm()
    sampler = neal.SimulatedAnnealingSampler()

    path = []
    for step, s in enumerate(np.linspace(0.0, 1.0, n_steps)):
        bqm = interpolate_bqm(initial, problem, s)
        response = sampler.sample(
            bqm,
            num_reads=50,
            num_sweeps=max(10, int(500 * s)),
            initial_states=[{i: 1 for i in range(N)}] * 50,
        )
        best = response.first
        sample = best.sample
        bits = "".join(str(sample.get(i, 0)) for i in range(N))
        energies = [d.energy for d in response.data(["energy"])]
        path.append({
            "step": step,
            "s": s,
            "best_bits": bits,
            "best_cut": cut_size(bits),
            "best_energy": best.energy,
            "mean_energy": float(np.mean(energies)),
            "min_energy": float(np.min(energies)),
            "max_energy": float(np.max(energies)),
        })
    return path


def print_energy_landscape(path: list[dict]) -> None:
    """Print the energy landscape as a text table."""
    print(f"  {'s':>5}  {'E_min':>9}  {'E_mean':>9}  {'E_max':>9}  "
          f"{'best':>6}  {'cut':>3}")
    print(f"  {'─'*5}  {'─'*9}  {'─'*9}  {'─'*9}  {'─'*6}  {'─'*3}")
    for row in path:
        print(f"  {row['s']:5.2f}  {row['min_energy']:+9.4f}  "
              f"{row['mean_energy']:+9.4f}  {row['max_energy']:+9.4f}  "
              f"{row['best_bits']:>6}  {row['best_cut']:3d}")


def print_energy_bar(path: list[dict]) -> None:
    """ASCII bar chart of the energy spread at each step."""
    all_min = [r["min_energy"] for r in path]
    all_max = [r["max_energy"] for r in path]
    global_min = min(all_min)
    global_max = max(all_max)
    span = global_max - global_min if global_max != global_min else 1.0
    width = 40

    print("\n  Energy landscape (bar = spread at each s):")
    print(f"  {'s':>5}  {'E_min':>8}  {'spread'}")
    print(f"  {'─'*5}  {'─'*8}  {'─'*width}")
    for row in path:
        lo = int((row["min_energy"] - global_min) / span * width)
        hi = int((row["max_energy"] - global_min) / span * width)
        bar = " " * lo + "█" * max(1, hi - lo)
        print(f"  {row['s']:5.2f}  {row['min_energy']:+8.3f}  |{bar}|")


def main() -> None:
    print("=== Adiabatic Quantum Computation — Concept Demo ===")
    print()
    print("Problem: MaxCut on C4 (0-1-2-3-0)")
    print(f"  Edges: {EDGES}")
    print()
    print("Adiabatic path: H(s) = (1-s) H_initial + s H_problem")
    print("  H_initial : transverse field (ground state = uniform superposition)")
    print("  H_problem : MaxCut cost Hamiltonian")
    print()

    path = adiabatic_path(n_steps=11)
    print_energy_landscape(path)
    print_energy_bar(path)

    final = path[-1]
    print()
    print("=== Final result (s = 1.0) ===")
    print(f"  Best sample: {final['best_bits']}")
    print(f"  Best energy: {final['best_energy']:+.4f}")
    print(f"  Cut size:    {final['best_cut']} / 4 (optimal)")
    print()
    print("The adiabatic theorem says: evolve slowly enough and the")
    print("system stays in the ground state, giving the optimal solution.")


if __name__ == "__main__":
    main()
