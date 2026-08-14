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
algorithms/
  shor/                     Shor period-finding, factor 15
  grover/                   Grover search
hybrid/
  qaoa/                     QAOA MaxCut
  tsp/                      traveling salesperson as a QUBO
  quantum-machine-learning/ hybrid variational classifier
```

## Setup

From this directory:

```bash
guix shell -m manifest.scm
uv sync --python python3
source env.sh
python -m ipykernel install --prefix=.venv --name=qiskit-workspace \
    --display-name="Qiskit workspace"
```

`uv sync` creates `.venv/` using the Guix `python3` and installs the
packages listed in `pyproject.toml`. `env.sh` puts the Guix profile on
`LD_LIBRARY_PATH` so NumPy / Aer (installed by uv as ordinary wheels)
can see `libz` and `libstdc++`.

## Run a script

Shortcut (enters the Guix shell, sources `env.sh`, then `uv run`):

```bash
chmod +x run
./run python basic/logic-gates/logic_gates.py
./run python basic/superposition/superposition.py
./run python basic/toffoli/toffoli.py
./run python algorithms/shor/shor.py
./run python algorithms/grover/grover.py
./run python hybrid/qaoa/qaoa.py
./run python hybrid/tsp/tsp.py
./run python hybrid/quantum-machine-learning/vqc.py
```

Or, by hand, still inside `guix shell -m manifest.scm` after `source env.sh`:

```bash
uv run python basic/logic-gates/logic_gates.py
```

## Notebooks

```bash
./run jupyter notebook
```

Open the `.ipynb` next to each script and pick the **Qiskit workspace**
kernel (it is the uv virtualenv). Each notebook is self-contained; it
does not import the sibling `.py` file.

## Notes

- All circuits run locally on Aer (or exact `Statevector` simulation).
  No IBM Quantum token is required.
- Qiskit prints bitstrings with qubit 0 on the **right**.
- The snippets are pedagogical: small instances (Shor factors 15,
  Grover searches 8 items, TSP is 4 cities with a fixed start).
