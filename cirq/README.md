# Cirq workspace

Standalone Google Cirq snippets for this repo. Separate from the
[`qiskit/`](../qiskit/) workspace: no shared package, no cross-imports.

| File | Topic |
|---|---|
| [`cirq-demo.py`](cirq-demo.py) / [`cirq-demo.ipynb`](cirq-demo.ipynb) | Explore `cirq.google` / `cirq_google` |
| [`cirq-fox.py`](cirq-fox.py) | Foxtail device grid |

### Basic topics

| Topic | Files | Description |
|---|---|---|
| [`basic/computational-basis/`](basic/computational-basis/) | `.py` + `.ipynb` | \|0⟩ and \|1⟩ states, measurement |
| [`basic/statevectors/`](basic/statevectors/) | `.py` + `.ipynb` | \|+⟩ state, state vector inspection, amplitudes |
| [`basic/logic-gates/`](basic/logic-gates/) | `.py` + `.ipynb` | X, Y, Z, H, S, T gates |
| [`basic/phase/`](basic/phase/) | `.py` + `.ipynb` | Global and relative phase |
| [`basic/superposition/`](basic/superposition/) | `.py` + `.ipynb` | Hadamard, 50/50 statistics, Bell pair |
| [`basic/bloch-sphere/`](basic/bloch-sphere/) | `.py` + `.ipynb` | Bloch sphere coordinates, rotations |
| [`basic/measurement/`](basic/measurement/) | `.py` + `.ipynb` | Z and X basis measurement |
| [`basic/tensor-products/`](basic/tensor-products/) | `.py` + `.ipynb` | 2-qubit tensor product states |
| [`basic/controlled-gates/`](basic/controlled-gates/) | `.py` + `.ipynb` | CNOT, CZ with truth tables |
| [`basic/entanglement/`](basic/entanglement/) | `.py` + `.ipynb` | Bell states, correlation measurements |
| [`basic/toffoli/`](basic/toffoli/) | `.py` + `.ipynb` | CCX gate, 3-qubit truth table |

## Setup

From **this directory** (`cirq/`, next to `pyproject.toml`):

```bash
export UV_PYTHON_PREFERENCE=only-system   # never let uv download a CPython
guix shell -m manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-cirq \
    --display-name="Qimono Kernel UV Cirq"
exit    # leave guix shell; host ls stays healthy
```

**Do not `source env.sh` in an interactive shell.** See the longer
explanation in [`qiskit/README.md`](../qiskit/README.md). Use `./run`:

```bash
chmod +x run
./run python cirq-demo.py
./run jupyter notebook
```

Open the `.ipynb` and pick the **Qimono Kernel UV Cirq** kernel.

Newer Cirq splits `cirq.google` into the separate `cirq_google`
package; the demo script falls back automatically.
