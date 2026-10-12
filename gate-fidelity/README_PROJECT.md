# Qimono Gate Fidelity: Randomized Benchmarking vs. Process Tomography

This project generates a radar chart to help explain the trade-offs between randomized benchmarking (RB) and process tomography in the MIT xPRO Introduction to Quantum Computing course.

> **Interpretation guardrail:** The ratings in `aspects.csv` are qualitative, illustrative teaching judgments, not experimental measurements or a universal ranking. The chart is a discussion aid. Suitability depends on the goal, implementation, and experimental setup.

## Project files

```text
gate-fidelity/
├── README_PROJECT.md
├── aspects.csv
├── pyproject.toml
└── randomized-benchmarking.py
```

- **`aspects.csv`** contains the comparison criteria, scores for each method, and notes explaining the ratings.
- **`randomized-benchmarking.py`** loads the CSV, validates the data, and draws the radar chart.
- **`pyproject.toml`** declares the Python project and its dependencies for `uv`.

## Requirements

Install [uv](https://docs.astral.sh/uv/) using the method recommended for your operating system. This project uses Python 3.11 or newer.

From the repository root, synchronize the project environment:

```bash
uv sync --project gate-fidelity
```

This creates or updates the project's virtual environment and lockfile from `pyproject.toml` / `uv.lock`.

## Generate the chart

Run from the repository root:

```bash
uv run --project gate-fidelity python gate-fidelity/randomized-benchmarking.py
```

By default, the chart is written to:

```text
gate-fidelity/gate-fidelity-radar.png
```

Choose a different CSV file or output path:

```bash
uv run --project gate-fidelity python gate-fidelity/randomized-benchmarking.py \
  --data gate-fidelity/aspects.csv \
  --output gate-fidelity/radar.png
```

If your Python environment supports a graphical display, add `--show` to display the chart interactively as well as save it:

```bash
uv run --project gate-fidelity python gate-fidelity/randomized-benchmarking.py --show
```

## Change the chart without editing Python

Edit `aspects.csv`. The required columns are:

| Column | Meaning |
|---|---|
| `criterion` | Label for a radar-chart axis |
| `randomized_benchmarking` | Score for randomized benchmarking |
| `process_tomography` | Score for process tomography |
| `higher_is_better` | Documentation flag describing the intended direction of the scale |
| `notes` | Rationale or qualification for the scores |

Scores must be numeric and between **1 and 5**. Use at least three criteria. Both methods should use the same scale and the same interpretation for each criterion. The plotting script reads the first three columns it requires; `higher_is_better` and `notes` are documentation fields and are not currently used to calculate or transform scores.

The existing values are deliberately qualitative. The course supports the broad trade-offs that RB is more efficient and less sensitive to state-preparation and measurement (SPAM) errors, while process tomography offers a more complete error characterization but scales poorly and is sensitive to SPAM errors. The course does not provide numerical ratings for these radar axes. The `Routine monitoring` axis is a proposed discussion dimension, not a directly quantified course result.

## Data validation and limitations

The script checks that the required CSV columns are present, criteria are not blank, scores are numeric and within the 1–5 range, and at least three criteria are supplied. It does not establish that a score is scientifically objective: the rationale in `notes` should be reviewed and revised as the discussion develops.

A radar chart is useful for comparing several dimensions at once, but polygon area is not a rigorous overall quality score. Do not infer a universal winner or a fixed qubit-count threshold from this visualization.

## Dependencies

The runtime dependencies are kept intentionally small:

- **NumPy**: calculates evenly spaced axis angles.
- **Matplotlib**: draws and exports the chart.
- **Python standard library**: reads CSV data, parses command-line options, and handles paths.

Pandas and SciPy are not required for the current task, so they are not included without a concrete use case.
