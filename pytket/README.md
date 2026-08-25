# pytket snippets

[pytket](https://github.com/CQCL/pytket) is a quantum circuit compiler and
optimizer from Cambridge Quantum (now Quantinuum). It provides a
framework-agnostic intermediate representation with powerful peephole
optimization passes, and converters for Qiskit, PennyLane, and other
frameworks.

These snippets demonstrate pytket's optimization capabilities:

- **optimization-qiskit** — Convert Qiskit circuits to pytket, optimize, convert back
- **optimization-pennylane** — Convert PennyLane circuits to pytket, optimize, convert back
- **standalone** — Build circuits natively in pytket and compare optimization levels

## Setup

```bash
guix shell -m manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-pytket \
    --display-name="Qimono Kernel pytket"
exit
```

Run scripts:

```bash
./run python optimization-qiskit/circuit-optimize/circuit_optimize.py
./run python optimization-pennylane/circuit-optimize/circuit_optimize.py
./run python standalone/native-circuits/native_circuits.py
```

Run notebooks with kernel `qimono-kernel-pytket`.
