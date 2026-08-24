# Cirq workspace

Standalone Google Cirq snippets for this repo. Separate from the
[`qiskit/`](../qiskit/) workspace: no shared package, no cross-imports.

| File | Topic |
|---|---|
| [`cirq-demo.py`](cirq-demo.py) / [`cirq-demo.ipynb`](cirq-demo.ipynb) | Explore `cirq.google` / `cirq_google` |
| [`cirq-fox.py`](cirq-fox.py) | Foxtail device grid |

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
