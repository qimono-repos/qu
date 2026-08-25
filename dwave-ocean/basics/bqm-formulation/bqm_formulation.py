#!/usr/bin/env python3
"""Binary Quadratic Model formulation with D-Wave Ocean.

Builds a small BQM with linear and quadratic terms, inspects its
structure, and visualizes the interaction graph with networkx.
"""

from __future__ import annotations

import dimod
import matplotlib.pyplot as plt
import networkx as nx


def build_bqm() -> dimod.BinaryQuadraticModel:
    bqm = dimod.BinaryQuadraticModel(
        {"a": -2.0, "b": -1.5, "c": 1.0, "d": 0.5},
        {("a", "b"): -1.0, ("b", "c"): 0.8, ("a", "c"): 0.5, ("c", "d"): -0.3},
        0.0,
        "SPIN",
    )
    return bqm


def inspect_bqm(bqm: dimod.BinaryQuadraticModel) -> None:
    print("=== BQM structure ===")
    print(f"  Variables: {list(bqm.variables)}")
    print(f"  Linear terms:      {dict(bqm.linear)}")
    print(f"  Quadratic terms:   {dict(bqm.quadratic)}")
    print(f"  Offset:            {bqm.offset}")
    print(f"  vartype:           {bqm.vartype}")
    print()


def evaluate_samples(bqm: dimod.BinaryQuadraticModel) -> None:
    print("=== Energy of a few spin configurations ===")
    samples = [
        {"a": 1, "b": 1, "c": -1, "d": 1},
        {"a": -1, "b": -1, "c": 1, "d": -1},
        {"a": 1, "b": -1, "c": 1, "d": 1},
    ]
    for s in samples:
        e = bqm.energy(s)
        print(f"  {s}  ->  E = {e:+.2f}")
    print()


def visualize_bqm(bqm: dimod.BinaryQuadraticModel) -> None:
    G = nx.Graph()
    for v in bqm.variables:
        G.add_node(v, bias=float(bqm.linear[v]))
    for (u, v), weight in bqm.quadratic.items():
        G.add_edge(u, v, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    biases = [G.nodes[n]["bias"] for n in G.nodes]
    edge_weights = [G.edges[e]["weight"] for e in G.edges]
    edge_colors = ["green" if w < 0 else "red" for w in edge_weights]
    node_sizes = [800 + 400 * abs(b) for b in biases]
    node_colors = ["lightblue" if b < 0 else "salmon" for b in biases]

    fig, ax = plt.subplots(figsize=(7, 5))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold")
    nx.draw_networkx_edges(G, pos, ax=ax, width=2, edge_color=edge_colors)
    edge_labels = {(u, v): f"{w:+.1f}" for (u, v), w in G.edges.items()}
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_size=10)
    ax.set_title("BQM interaction graph\n(blue = negative bias, red = positive bias)")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("bqm_graph.png", dpi=150)
    print("Saved bqm_graph.png")


def main() -> None:
    bqm = build_bqm()
    inspect_bqm(bqm)
    evaluate_samples(bqm)
    visualize_bqm(bqm)


if __name__ == "__main__":
    main()
