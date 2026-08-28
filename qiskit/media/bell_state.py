#!/usr/bin/env python3
"""Render the Bell state notes: the H-CX circuit (fig-001).

A two-panel matplotlib figure written as SVG to the repo-level `assets/`
directory: on the left the generating circuit (H on q0, CNOT q0->q1) and
on the right the exact measurement probabilities of the four
computational-basis states. Writing SVG keeps the figure crisp at any
size for the repo docs.
"""

from __future__ import annotations

import argparse
import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import qiskit as qk  # noqa: E402
import qiskit.quantum_info as qki  # noqa: E402


def bell_state() -> qki.Statevector:
    qc = qk.QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qki.Statevector.from_instruction(qc)


def render_figure(out_path: pathlib.Path) -> None:
    labels = [r"$|00\rangle$", r"$|01\rangle$", r"$|10\rangle$", r"$|11\rangle$"]
    probs = np.abs(bell_state().data) ** 2

    fig = plt.figure(figsize=(9, 4))

    ax_circuit = fig.add_axes([0.02, 0.10, 0.44, 0.80])
    ax_circuit.axis("off")
    qc = qk.QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.draw(output="mpl", ax=ax_circuit, initial_state=True, scale=0.9)

    ax_prob = fig.add_axes([0.55, 0.10, 0.43, 0.80])
    active = [p > 0 for p in probs]
    colors = ["#2f6fb2" if on else "#cfd6dd" for on in active]
    bars = ax_prob.bar(labels, probs, color=colors, width=0.55)
    ax_prob.set_ylim(0, 0.62)
    ax_prob.set_ylabel("probability")
    ax_prob.axhline(0.5, ls="--", c="#999", lw=0.9)
    ax_prob.spines[["top", "right"]].set_visible(False)
    ax_prob.tick_params(axis="x", labelsize=11)
    for bar, p in zip(bars, probs):
        if p > 0:
            ax_prob.annotate(
                r"$1/\sqrt{2}$" if p == 0.5 else f"{p:.3f}",
                xy=(bar.get_x() + bar.get_width() / 2, p),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                fontsize=11,
                color="#1c4a80",
                fontweight="bold",
            )

    fig.suptitle(
        r"$|\Phi^{+}\rangle = \frac{1}{\sqrt{2}}\left(|00\rangle + |11\rangle\right)$"
        "   —   the Bell state from   H  then  CNOT",
        y=0.98,
        fontsize=13,
    )
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    default_out = pathlib.Path(__file__).resolve().parents[2] / "assets" / "fig-001.svg"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=default_out,
        help=f"output SVG path (default: {default_out})",
    )
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    render_figure(args.out)
    print(f"wrote {args.out} ({args.out.stat().st_size / 1024:.1f} KiB)")


if __name__ == "__main__":
    main()