#!/usr/bin/env python3
"""Generate a radar-chart comparison of process tomography and randomized benchmarking.

Qimono / Gate Fidelity study artifact
=====================================

IMPORTANT INTERPRETATION NOTE
-----------------------------
The scores in this chart are qualitative, illustrative ratings used to visualize
the trade-offs described in the MIT xPRO Introduction to Quantum Computing
course material. They are NOT experimental measurements, a literature-derived
benchmark, or a universal ranking of these techniques. In particular, the chart
does not imply a fixed qubit-count threshold at which one method should replace
the other.

Course-grounded distinctions represented here:
- Randomized benchmarking (RB) is presented as more efficient than process
  tomography and insensitive to state-preparation and measurement (SPAM) errors.
- RB estimates aggregate/net error but does not identify individual error
  channels.
- Process tomography provides a more complete characterization of gate errors,
  but its measurement requirements scale poorly as the number of qubits grows,
  and it is sensitive to state-preparation and measurement errors.

Install dependencies:
    python -m pip install matplotlib numpy

Run:
    python gate-fidelity/randomized-benchmarking.py
    python gate-fidelity/randomized-benchmarking.py --output gate-fidelity/radar.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# Qualitative ratings on a 1-5 scale, based on the course's stated trade-offs.
# These are author-assigned illustrative values, not measured facts.
CRITERIA = [
    "Efficiency",
    "Scalability",
    "Diagnostic\ndetail",
    "SPAM-error\nrobustness",
    "Routine\nmonitoring",
]

RATINGS = {
    "Randomized benchmarking": [5, 5, 2, 4, 4],
    "Process tomography": [2, 1, 5, 1, 3],
}


def make_radar_chart(output: Path, show: bool = False) -> Path:
    """Create and save the radar chart, returning the output path."""
    count = len(CRITERIA)
    angles = np.linspace(0, 2 * np.pi, count, endpoint=False).tolist()
    closed_angles = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(9.5, 7.2), subplot_kw={"polar": True})
    fig.patch.set_facecolor("#08090d")
    ax.set_facecolor("#08090d")

    # Start at the top and proceed clockwise.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles)
    ax.set_xticklabels(CRITERIA, color="#f1eef6", fontsize=11)
    ax.tick_params(axis="x", pad=16)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], color="#aaa6b4", fontsize=9)
    ax.set_rlabel_position(12)
    ax.grid(color="#55515e", alpha=0.42, linewidth=0.8)
    ax.spines["polar"].set_color("#686371")
    ax.spines["polar"].set_alpha(0.5)

    styles = {
        "Randomized benchmarking": {
            "color": "#f27fc3",
            "marker": "o",
            "linewidth": 2.6,
            "alpha": 0.19,
        },
        "Process tomography": {
            "color": "#5b9cff",
            "marker": "o",
            "linewidth": 2.6,
            "alpha": 0.17,
        },
    }

    for name, values in RATINGS.items():
        style = styles[name]
        closed_values = values + values[:1]
        ax.plot(
            closed_angles,
            closed_values,
            color=style["color"],
            linewidth=style["linewidth"],
            marker=style["marker"],
            markersize=6,
            label=name,
        )
        ax.fill(
            closed_angles,
            closed_values,
            color=style["color"],
            alpha=style["alpha"],
        )

    fig.suptitle(
        "GATE FIDELITY  /  METHOD TRADE-OFFS",
        color="#f7f3fb",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )
    fig.text(
        0.5,
        0.925,
        "Qualitative teaching illustration • scale 1–5 • higher is more favorable",
        ha="center",
        color="#bdb8c7",
        fontsize=9,
    )

    legend = ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, -0.20),
        ncol=2,
        frameon=False,
        fontsize=10,
        labelcolor="#e8e4ed",
    )
    for handle in legend.legend_handles:
        handle.set_linewidth(3)

    fig.text(
        0.5,
        0.025,
        "Illustrative ratings, not experimental data. Suitability depends on the measurement goal and setup.",
        ha="center",
        color="#ffb98f",
        fontsize=8.5,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180, facecolor=fig.get_facecolor(), bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the Qimono gate-fidelity radar chart."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("gate-fidelity-radar.png"),
        help="Output image path (default: next to this script).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the chart interactively after saving it.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = make_radar_chart(args.output, show=args.show)
    print(f"Radar chart saved to: {output}")


if __name__ == "__main__":
    main()
