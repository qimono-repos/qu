# Quantum circuits in Python

`superposition-stats`: equal-superposition stats for n qubits (H^⊗n |0…0⟩). Managed with `uv`. Uses numpy; it does not need Qiskit.

## Run

From this directory:

```bash
uv run superposition-stats 4
uv run --extra test pytest
```

Output:

```
n=4: summands=16, amplitude=0.250000, P per outcome=0.062500
```

## API

`superposition_stats(n)` returns `(summands, amplitude, probability_per_outcome)` and raises `ValueError` for n < 1.
The tests assert the 3-qubit (8, 1/√8, 1/8) and 4-qubit (16, 1/4, 1/16) cases.
