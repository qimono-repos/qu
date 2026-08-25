# PyQuil snippets

PyQuil is Rigetti's Python library for quantum programming using the
**Quil** instruction language. Quil programs are compiled by **quilc**
and executed on the **QVM** (Quantum Virtual Machine) simulator.

## Prerequisites

PyQuil requires two background servers:

| Server | Purpose | Default port |
|--------|---------|-------------|
| `quilc` | Quil compiler | 5000 |
| `QVM` | Quantum simulator | 5001 |

### Option A: Docker (recommended)

```bash
docker run --rm -p 5000:5000 rigetti/quilc &
docker run --rm -p 5001:5001 rigetti/qvm &
```

### Option B: Install from source

Requires Rust toolchain. See Rigetti docs for build instructions.

### Option C: Rigetti QCS

For real hardware access, sign up at
[Quantum Cloud Services](https://qcs.rigetti.com/).

## Setup

```bash
guix shell -m manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv \
    --name=qimono-kernel-pyquil \
    --display-name="Qimono Kernel PyQuil"
exit
```

Run scripts with `./run python <path>`. Notebooks use kernel
`qimono-kernel-pyquil`.

## Connecting to local QVM

```python
from pyquil import Program, get_qc

qc = get_qc("2q-qvm")  # connects to localhost:5001
```

`get_qc("Nq-qvm")` connects to a local QVM server running on
port 5001 and a quilc compiler on port 5000.

## Topics

```
pyquil/basics/bell-state        # Bell pair on 2 qubits
pyquil/basics/ghz-state         # 4-qubit GHZ state
pyquil/circuits/parameterized   # Parameterized RZ rotations
```
