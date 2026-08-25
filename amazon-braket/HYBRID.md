# Hybrid classical-quantum approach

Amazon Braket supports **hybrid quantum-classical workflows** where classical
compute orchestrates quantum tasks on AWS.

## When to use hybrid

| Problem type | Classical role | Quantum role | Example |
|---|---|---|---|
| Variational algorithms | Optimize parameters | Run quantum circuit | VQE, QAOA |
| Quantum ML | Train model | Evaluate quantum kernel | Hybrid ML |
| Circuit optimization | Search circuit structure | Evaluate fidelity | Circuit knitting |

## Braket hybrid examples

- `hybrid/variational/` — Variational algorithm using local simulator

## Key pattern

Braket hybrid uses **Amazon Braket Hybrid Jobs** for managed execution:

```python
from braket.devices import LocalSimulator
from braket.circuit import Circuit

# Classical setup
device = LocalSimulator()

# Quantum circuit
bell = Circuit().h(0).cnot(0, 1)

# Run quantum task
result = device.run(bell, shots=1000).result()
```

For real hybrid workloads, use Braket Hybrid Jobs with PennyLane or
custom classical drivers.
