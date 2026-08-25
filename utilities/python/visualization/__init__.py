"""Shared visualization utilities for quantum circuits.

Provides helpers to save circuit diagrams, Bloch sphere plots,
and probability distributions as PNG + SVG.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import qiskit as qk

from qiskit.visualization import (
    plot_bloch_multivector,
    plot_distribution,
)


OUTPUT_DIR = Path("output")


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(fig, name: str, dpi: int = 200) -> None:
    ensure_output_dir()

    png_path = OUTPUT_DIR / f"{name}.png"
    svg_path = OUTPUT_DIR / f"{name}.svg"

    fig.savefig(
        png_path,
        dpi=dpi,
        bbox_inches="tight",
    )

    fig.savefig(
        svg_path,
        bbox_inches="tight",
    )

    print(f"Saved → {png_path}")
    print(f"Saved → {svg_path}")

    plt.close(fig)


def save_circuit(qc: qk.QuantumCircuit, name: str = "circuit") -> None:
    fig = qc.draw(
        output="mpl",
        fold=-1,
        idle_wires=True,
        initial_state=True,
    )

    save_figure(fig, name)


def save_bloch(
    qc: qk.QuantumCircuit,
    name: str = "bloch",
) -> None:
    sv = qk.quantum_info.Statevector.from_instruction(qc)

    fig = plot_bloch_multivector(sv)

    save_figure(fig, name)


def save_distribution(
    probabilities: dict[str, float],
    name: str = "distribution",
) -> None:
    fig = plot_distribution(probabilities)

    save_figure(fig, name)
