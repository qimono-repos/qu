# Hybrid classical-quantum approach

PennyLane's core design is **hybrid classical-quantum** — quantum nodes are
differentiable and integrated into classical autograd pipelines.

## When to use hybrid

| Problem type | Classical role | Quantum role | Example |
|---|---|---|---|
| Variational algorithms | Optimize cost function | Prepare parameterized state | VQE, QAOA |
| Quantum ML | Train classical layers | Evaluate quantum feature map | QML classifier |
| Gradients | Backpropagation | Parameter-shift rule | `qml.grad()` |
| Optimization | Adam/SGD optimizer | Quantum circuit forward pass | QAOA MaxCut |

## PennyLane hybrid examples

- `qiskit-compatibility/qaoa-max-cut/` — QAOA with PennyLane's autograd
- `features/gradients/` — Gradient computation (parameter-shift, backprop)
- `features/qml-classifier/` — Quantum-classical neural network

## Key pattern

PennyLane uses **automatic differentiation** — no manual gradient computation:

```python
dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev, diff_method="parameter-shift")
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

grad_fn = qml.grad(circuit)  # automatic gradient
```
