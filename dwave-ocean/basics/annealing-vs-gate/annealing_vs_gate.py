#!/usr/bin/env python3
"""Simulated annealing (D-Wave Ocean) vs gate-model QAOA on the same problem.

Solves a small MaxCut instance on C4 (4-cycle) with both:
  1. dwave-neal SimulatedAnnealingSampler (classical annealing)
  2. Qiskit QAOA (variational gate-model algorithm)
and compares the results side by side.
"""

from __future__ import annotations

import dimod
import neal
import networkx as nx
import numpy as np
import qiskit as qk
import scipy as scp


EDGES = [(0, 1), (1, 2), (2, 3), (3, 0)]
N = 4
P = 2


def cut_size(bits: str) -> int:
    colors = [int(b) for b in bits[::-1]]
    return sum(colors[i] != colors[j] for i, j in EDGES)


def build_bqm() -> dimod.BinaryQuadraticModel:
    bqm = dimod.BinaryQuadraticModel("SPIN")
    for i, j in EDGES:
        bqm.add_variable(i, 0.0)
        bqm.add_variable(j, 0.0)
        bqm.add_interaction(i, j, -1.0)
    return bqm


def solve_simulated_annealing(num_reads: int = 100) -> tuple[str, float, dict[str, float]]:
    bqm = build_bqm()
    sampler = neal.SimulatedAnnealingSampler()
    response = sampler.sample(bqm, num_reads=num_reads, num_sweeps=500)
    sample = response.first.sample
    energy = response.first.energy
    bits = "".join(str(sample.get(i, 0)) for i in range(N))
    energies = {}
    for bits_key in set(
        "".join(str(s.get(i, 0)) for i in range(N)) for s in response.samples()
    ):
        pass
    return bits, energy, {}


def build_qaoa_circuit(params: np.ndarray) -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(N)
    qc.h(range(N))
    for k in range(P):
        gamma = float(params[k])
        beta = float(params[P + k])
        for i, j in EDGES:
            qc.cx(i, j)
            qc.rz(2 * gamma, j)
            qc.cx(i, j)
        for q in range(N):
            qc.rx(2 * beta, q)
    return qc


def expected_cut(params: np.ndarray) -> float:
    qc = build_qaoa_circuit(params)
    probs = qk.quantum_info.Statevector.from_instruction(qc).probabilities_dict()
    return sum(p * cut_size(b) for b, p in probs.items())


def solve_qaoa() -> tuple[str, float]:
    rng = np.random.default_rng(7)
    guess = rng.uniform(0, np.pi, size=2 * P)
    opt = scp.optimize.minimize(
        lambda p: -expected_cut(p),
        guess,
        method="COBYLA",
        options={"maxiter": 80, "rhobeg": 0.4},
    )
    qc = build_qaoa_circuit(opt.x)
    probs = qk.quantum_info.Statevector.from_instruction(qc).probabilities_dict()
    bits, p = max(probs.items(), key=lambda kv: kv[1])
    exp_cut = expected_cut(opt.x)
    return bits, exp_cut


def main() -> None:
    print("=== Problem: MaxCut on C4 (0-1-2-3-0) ===")
    print(f"  Edges: {EDGES}")
    print()

    sa_bits, sa_energy, _ = solve_simulated_annealing()
    sa_cut = cut_size(sa_bits)
    print("=== Simulated annealing (dwave-neal) ===")
    print(f"  Best sample:  {sa_bits}")
    print(f"  BQM energy:   {sa_energy:+.2f}")
    print(f"  Cut value:    {sa_cut}")
    print()

    qaoa_bits, qaoa_exp = solve_qaoa()
    qaoa_cut = cut_size(qaoa_bits)
    print("=== Qiskit QAOA (gate-model) ===")
    print(f"  Most likely:  |{qaoa_bits}>")
    print(f"  Expected cut: {qaoa_exp:.3f}")
    print(f"  Cut value:    {qaoa_cut}")
    print()

    print("=== Comparison ===")
    print(f"  Simulated annealer cut: {sa_cut}")
    print(f"  QAOA cut:               {qaoa_cut}")
    print(f"  Optimal cut on C4:      {4}")


if __name__ == "__main__":
    main()
