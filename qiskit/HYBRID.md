# Hybrid classical-quantum approach

This framework supports **hybrid classical-quantum algorithms** where a classical
optimizer iteratively adjusts parameters of a quantum circuit.

## When to use hybrid

| Problem type | Classical role | Quantum role | Example |
|---|---|---|---|
| Variational algorithms | Optimize cost function | Prepare parameterized state | VQE, QAOA |
| Quantum machine learning | Train classical weights | Evaluate quantum feature map | VQC, QML |
| Optimization | Search parameter space | Evaluate objective on quantum hardware | MaxCut, TSP |
| Error mitigation | Post-processing | Raw noisy measurements | ZNE, PEC |

## Qiskit hybrid examples

- `optimization/qaoa/` — QAOA for MaxCut (classical optimizer + quantum circuit)
- `optimization/tsp/` — Traveling salesperson (classical search + quantum evaluation)
- `machinelearning/vqc/` — Variational quantum classifier

## Key pattern

```
while not converged:
    1. Run quantum circuit with current parameters → get measurement
    2. Compute cost/loss from measurement results
    3. Update parameters using classical optimizer (COBYLA, L-BFGS-B, etc.)
```

The quantum circuit acts as an **objective function evaluator** — the classical
optimizer does the heavy lifting of parameter search.
