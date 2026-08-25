# Visualization utilities

Shared Python helpers for saving quantum circuit diagrams, Bloch sphere plots,
and probability distributions as PNG + SVG.

## Usage

```python
from visualization import save_circuit, save_bloch, save_distribution

save_circuit(qc, "my_circuit")
save_bloch(qc, "my_bloch")
save_distribution(probabilities, "my_distribution")
```

Output goes to `./output/` (created automatically).

## Requirements

- `qiskit` (for circuit drawing and statevector)
- `matplotlib` (for figure rendering)

These are already in the shared `requirements.txt` at the repo root.
