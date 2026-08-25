#!/usr/bin/env python3
"""MaxCut on a 4-cycle (C4) using D-Wave Ocean.

Formulates MaxCut as a BQM, samples with neal.SimulatedAnnealingSampler,
and visualizes the best cut.  Also shows what Qiskit QAOA would give.
"""

from __future__ import annotations

import dimod
import matplotlib.pyplot as plt
import neal
import networkx as nx
import numpy as np
import qiskit as qk
import scipy as scp

EDGES = [(0, 1), (1, 2), (2, 3), (3, 0)]
N = 4


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


def solve_ocean(bqm: dimod.BinaryQuadraticModel) -> dict:
    sampler = neal.SimulatedAnnealingSampler()
    response = sampler.sample(bqm, num_reads=200, num_sweeps=500)
    sample = response.first.sample
    bits = "".join(str(sample.get(i, 0)) for i in range(N))
    return {"bits": bits, "cut": cut_size(bits), "energy": response.first.energy}


def solve_qiskit_qaoa() -> dict:
    P = 2

    def cost_layer(gamma):
        qc = qk.QuantumCircuit(N)
        for i, j in EDGES:
            qc.cx(i, j)
            qc.rz(2 * gamma, j)
            qc.cx(i, j)
        return qc

    def mixer_layer(beta):
        qc = qk.QuantumCircuit(N)
        for q in range(N):
            qc.rx(2 * beta, q)
        return qc

    def circuit(params):
        qc = qk.QuantumCircuit(N)
        qc.h(range(N))
        for k in range(P):
            qc.compose(cost_layer(float(params[k])), inplace=True)
            qc.compose(mixer_layer(float(params[P + k])), inplace=True)
        return qc

    def expected(params):
        probs = qk.quantum_info.Statevector.from_instruction(circuit(params)).probabilities_dict()
        return sum(p * cut_size(b) for b, p in probs.items())

    rng = np.random.default_rng(7)
    guess = rng.uniform(0, np.pi, size=2 * P)
    opt = scp.optimize.minimize(
        lambda p: -expected(p), guess, method="COBYLA",
        options={"maxiter": 80, "rhobeg": 0.4},
    )
    probs = qk.quantum_info.Statevector.from_instruction(circuit(opt.x)).probabilities_dict()
    bits, p = max(probs.items(), key=lambda kv: kv[1])
    return {"bits": bits, "cut": cut_size(bits), "prob": p, "expected": expected(opt.x)}


def visualize_cut(bits: str) -> None:
    colors = [int(b) for b in bits[::-1]]
    color_map = ["lightblue" if c == 0 else "salmon" for c in colors]
    pos = {0: (0, 1), 1: (1, 1), 2: (1, 0), 3: (0, 0)}
    G = nx.cycle_graph(N)

    fig, ax = plt.subplots(figsize=(5, 5))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=color_map, node_size=800)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=14, font_weight="bold")
    cut_edges = [(i, j) for i, j in EDGES if colors[i] != colors[j]]
    uncut_edges = [(i, j) for i, j in EDGES if colors[i] == colors[j]]
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=cut_edges, width=3, edge_color="green", style="solid")
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=uncut_edges, width=2, edge_color="gray", style="dashed")
    ax.set_title(f"MaxCut on C4  cut={cut_size(bits)}")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("maxcut_c4.png", dpi=150)
    print("Saved maxcut_c4.png")


def main() -> None:
    bqm = build_bqm()
    print("=== BQM ===")
    print(f"  Linear:      {dict(bqm.linear)}")
    print(f"  Quadratic:   {dict(bqm.quadratic)}")
    print()

    ocean = solve_ocean(bqm)
    print("=== D-Wave Ocean (simulated annealing) ===")
    print(f"  Best:  {ocean['bits']}  cut={ocean['cut']}  energy={ocean['energy']:+.2f}")
    print()

    qaoa = solve_qiskit_qaoa()
    print("=== Qiskit QAOA (gate-model) ===")
    print(f"  Best:  |{qaoa['bits']}>  cut={qaoa['cut']}  P={qaoa['prob']:.3f}  exp={qaoa['expected']:.3f}")
    print()

    visualize_cut(ocean["bits"])


if __name__ == "__main__":
    main()
