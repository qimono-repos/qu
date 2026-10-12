#!/usr/bin/env python3
"""Generate a Qimono radar chart comparing gate-fidelity methods.

The ratings are qualitative teaching illustrations, not experimental data or a
universal ranking. Edit aspects.csv to change criteria and scores.

Install:
    python -m pip install matplotlib numpy

Run from the repository root:
    python gate-fidelity/randomized-benchmarking.py
    python gate-fidelity/randomized-benchmarking.py --data gate-fidelity/aspects.csv
    python gate-fidelity/randomized-benchmarking.py --output gate-fidelity/radar.png
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


METHODS = {
    "Randomized benchmarking": {
        "column": "randomized_benchmarking",
        "color": "#f27fc3",
        "alpha": 0.19,
    },
    "Process tomography": {
        "column": "process_tomography",
        "color": "#5b9cff",
        "alpha": 0.17,
    },
}


def load_chart_data(data_path: Path) -> tuple[list[str], dict[str, list[float]]]:
    """Read criteria and scores from CSV; reject malformed or out-of-range data."""
    criteria: list[str] = []
    ratings = {name: [] for name in METHODS}
    required = {"criterion", *(item["column"] for item in METHODS.values())}

    with data_path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            missing = required - set(reader.fieldnames or [])
            raise ValueError(
                f"CSV is missing required column(s): {', '.join(sorted(missing))}"
            )

        for line_number, row in enumerate(reader, start=2):
            criterion = (row.get("criterion") or "").strip()
            if not criterion:
                raise ValueError(f"CSV line {line_number}: criterion cannot be blank.")

            criteria.append(criterion)
            for method, settings in METHODS.items():
                try:
                    score = float(row[settings["column"]])
                except (TypeError, ValueError) as exc:
                    raise ValueError(
                        f"CSV line {line_number}: {settings['column']} must be numeric."
                    ) from exc
                if not 1 <= score <= 5:
                    raise ValueError(
                        f"CSV line {line_number}: scores must be between 1 and 5."
                    )
                ratings[method].append(score)

    if len(criteria) < 3:
        raise ValueError("A radar chart needs at least three criteria.")
    return criteria, ratings


def make_radar_chart(data_path: Path, output: Path, show: bool = False) -> Path:
    """Generate and save the chart from CSV data."""
    criteria, ratings = load_chart_data(data_path)
    count = len(criteria)
    angles = np.linspace(0, 2 * np.pi, count, endpoint=False).tolist()
    closed_angles = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(9.5, 7.2), subplot_kw={"polar": True})
    fig.patch.set_facecolor("#08090d")
    ax.set_facecolor("#08090d")
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles)
    labels = [
        label.replace(" ", "\n", 1) if len(label) > 17 else label
        for label in criteria
    ]
    ax.set_xticklabels(labels, color="#f1eef6", fontsize=11)
    ax.tick_params(axis="x", pad=16)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], color="#aaa6b4", fontsize=9)
    ax.set_rlabel_position(12)
    ax.grid(color="#55515e", alpha=0.42, linewidth=0.8)
    ax.spines["polar"].set_color("#686371")
    ax.spines["polar"].set_alpha(0.5)

    for name, settings in METHODS.items():
        values = ratings[name]
        closed_values = values + values[:1]
        ax.plot(
            closed_angles,
            closed_values,
            color=settings["color"],
            linewidth=2.6,
            marker="o",
            markersize=6,
            label=name,
        )
        ax.fill(
            closed_angles,
            closed_values,
            color=settings["color"],
            alpha=settings["alpha"],
        )

    # Reserve space so the title and top axis label do not collide.
    fig.subplots_adjust(top=0.78, bottom=0.27, left=0.08, right=0.92)
    fig.suptitle(
        "GATE FIDELITY  /  METHOD TRADE-OFFS",
        color="#f7f3fb",
        fontsize=16,
        fontweight="bold",
        y=0.975,
    )
    fig.text(
        0.5,
        0.90,
        "Qualitative teaching illustration • scale 1–5 • higher is more favorable",
        ha="center",
        color="#bdb8c7",
        fontsize=9,
    )

    legend = ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, -0.16),
        ncol=2,
        frameon=False,
        fontsize=10,
        labelcolor="#e8e4ed",
    )
    for handle in legend.legend_handles:
        handle.set_linewidth(3)

    fig.text(
        0.5,
        0.035,
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
        description="Generate the Qimono gate-fidelity radar chart from CSV."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=Path(__file__).with_name("aspects.csv"),
        help="CSV data file (default: aspects.csv next to this script).",
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
    output = make_radar_chart(args.data, args.output, show=args.show)
    print(f"Radar chart saved to: {output}")


if __name__ == "__main__":
    main()
