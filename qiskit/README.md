# Qiskit workspace

A collection of **standalone** Qiskit snippets. Every topic is its own
folder with a `.py` script and a matching Jupyter notebook. Nothing is
imported across folders.

Host toolchain (Ubuntu + [Guix](https://guix.gnu.org/)):

- Python comes from Guix
- `uv` comes from Guix
- Qiskit, Aer, NumPy, SciPy, Matplotlib, and Jupyter are installed by `uv`

## Layout

```
basic/
  logic-gates/              Pauli, phase, Hadamard, CX, SWAP
  superposition/            Hadamard + CX (Bell pair)
  toffoli/                  CCX / controlled-controlled-NOT
big-o/
  constant.py / .ipynb      O(1) list/dict access
  logarithm.py / .ipynb     O(log n) binary search
algorithms/
  shor/                     Shor period-finding, factor 15
  grover/                   Grover search
  deutsch-jozsa/            constant vs balanced, n=2
hybrid/
  qaoa/                     QAOA MaxCut
  tsp/                      traveling salesperson as a QUBO
  quantum-machine-learning/ hybrid variational classifier
```

## Setup

From **this directory** (`qiskit/`, next to `pyproject.toml`):

```bash
export UV_PYTHON_PREFERENCE=only-system   # never let uv download a CPython
guix shell -m manifest.scm
uv sync --python python3
# still inside the guix shell, still *without* sourcing env.sh:
python -m ipykernel install --prefix=.venv --name=qiskit-workspace \
    --display-name="Qiskit workspace"
exit    # leave guix shell; host ls stays healthy
```

`uv sync` creates `.venv/` using the Guix `python3` and installs the
packages listed in `pyproject.toml`.

**Do not `source env.sh` in an interactive shell.** That file puts the
Guix profile on `LD_LIBRARY_PATH` so NumPy / Aer can see `libz` and
`libstdc++`. Ubuntu `ls` then loads Guix `libm` and dies with
`GLIBC_2.43 not found`. `./run` sources `env.sh` only in a throwaway
child process, then `uv run` — your prompt is never polluted. `exit`
from a broken `guix shell` restores `ls`.

## Run a script

Preferred (Guix + `env.sh` + venv, no prompt side effects):

```bash
chmod +x run
./run python basic/logic-gates/logic_gates.py
./run python basic/superposition/superposition.py
./run python basic/toffoli/toffoli.py
./run python big-o/constant.py
./run python big-o/logarithm.py
./run python algorithms/shor/shor.py
./run python algorithms/grover/grover.py
./run python algorithms/deutsch-jozsa/deutsch_jozsa.py
./run python hybrid/qaoa/qaoa.py
./run python hybrid/tsp/tsp.py
./run python hybrid/quantum-machine-learning/vqc.py
```

Optional conda-style prompt (does **not** set `LD_LIBRARY_PATH`):

```bash
source .venv/bin/activate    # prompt becomes (qiskit-workspace)
# still run code with ./run, not bare `python`, so Aer sees Guix libs
./run python basic/logic-gates/logic_gates.py
deactivate
```

## Notebooks

```bash
./run jupyter notebook
```

Open the `.ipynb` next to each script and pick the **Qiskit workspace**
kernel (it is the uv virtualenv). Each notebook is self-contained; it
does not import the sibling `.py` file.

### VS Code (Jupyter extension)

The notebook JSON only stores a **name** (`qiskit-workspace`). It does
not contain Qiskit. The packages live in `qiskit/.venv/`.

After `uv sync` on this machine, register the kernel once (not committed):

```bash
cd qiskit
.venv/bin/python -m ipykernel install --user --name=qiskit-workspace \
    --display-name="Qimono Jupyter Kernel"
```

That writes `~/.local/share/jupyter/kernels/qiskit-workspace/` and
points at **this** clone’s `.venv`. Reload the VS Code window.

In **Select Another Kernel**:

| Menu | Pick | What you get |
|------|------|----------------|
| **Jupyter Kernel…** | **Qiskit workspace** | the venv (Qiskit, Aer, …) |
| **Python Environments…** | `qiskit/.venv/bin/python` | same venv, unlabeled |
| Python Environments… | `/gnu/store/…/python3` | Guix Python **without** Qiskit |
| Python Environments… | `/usr/bin/python3` | Ubuntu OS Python, no Qiskit |

Do **not** pick the raw `/gnu/store` interpreter. It is the same 3.11
as the venv, but the wheels are only inside `.venv`.

## Notes

- All circuits run locally on Aer (or exact `Statevector` simulation).
  No IBM Quantum token is required.
- Qiskit prints bitstrings with qubit 0 on the **right**.
- The snippets are pedagogical: small instances (Shor factors 15,
  Grover searches 8 items, TSP is 4 cities with a fixed start).
