# Week 4 local Qiskit workspace

Local, offline-first workspace for MIT xPRO QCFx1 Week 4: **A Simple Quantum
Algorithm in Practice**. This folder follows the repo's `uv`-per-project style
and the specs in `specs/week-4/`. It is a study and checking environment, not a
generator of graded answers.

> **Lab gate:** do not commit the four N=1 Deutsch-Jozsa oracles
> (`f = 00, 11, 01, 10`, built only with `X` and `CNOT`), graded lab solutions,
> or quiz answers before the lab is submitted.

Time reference: **Paramaribo (America/Paramaribo, UTC−3, no DST)**. Hard deadline:
**Mon 2026-11-02 20:30 Paramaribo** (23:30 UTC).

## Setup

From the repository root:

```bash
uv sync --project week-4

# One-time per environment: register the project kernel used by the notebooks.
uv run --project week-4 python -m ipykernel install --sys-prefix \
  --name qimono-week-4 --display-name "Qimono Week 4"
```

The notebooks select the `Qimono Week 4` kernel, so they use this project's
`qiskit` rather than a global Python. Re-run the install command if you delete
`week-4/.venv` and recreate it.

Smoke test:

```bash
uv run --project week-4 python -c "import qiskit; print(qiskit.__version__)"
```

Open the notebooks:

```bash
uv run --project week-4 jupyter lab week-4/notebooks
```

The notebooks also work if you launch Jupyter from inside `week-4/`.

## Notebooks

| Notebook | Covers | What to do |
|---|---|---|
| `01-classical-vs-quantum-circuit-model.ipynb` | V1/V2 | Classical full adder, initialize → compute → measure, Hadamard superposition, normalization, measurement |
| `02-deutsch-jozsa.ipynb` | V3 | Deutsch-Jozsa, phase kickback, interference, query-count table, oracle-checking helpers |
| `03-software-stack-and-qcvv.ipynb` | V4a/V4b | Software-stack analogies, control vs processing, RB vs gate-set tomography, a toy noise experiment |
| `04-ibm-q-composer-qasm.ipynb` | V5 | OpenQASM, Composer-era connectivity, CNOT direction flip, transpilation, guarded IBM Quantum example |

The four N=1 oracles are deliberately **not** included. Notebook 2 provides a
place to drop in an oracle you wrote, plus `oracle_truth_table()` and
`is_constant_or_balanced()` to check it after the lab.

## qasm-check

`qasm_check.py` implements `specs/week-4/qasm-check.spec.md`: it loads a
hand-written `.qasm` file, simulates it, and checks your prediction. It does not
generate or fix circuits.

From the repository root:

```bash
# Draw and simulate
uv run --project week-4 python week-4/qasm_check.py week-4/practice/katas/k1.qasm --draw

# Check a predicted distribution
uv run --project week-4 python week-4/qasm_check.py week-4/practice/katas/bell.qasm \
  --expect "00:0.5,11:0.5"

# Compare two circuits up to global phase
uv run --project week-4 python week-4/qasm_check.py equiv a.qasm b.qasm
```

Or use the wrapper (it calls `uv run --project week-4` for you):

```bash
week-4/qasm-check week-4/practice/katas/k1.qasm --expect "0:1.0"
```

Use `--qasm3` for OpenQASM 3, `--statevector` for exact amplitudes, `--shots`
and `--seed` for reproducible counts. Exit codes: `0` pass, `1` fail,
`2` parse or input error.

Run the acceptance tests:

```bash
uv run --project week-4 pytest week-4/tests
```

## IBM Quantum (optional)

The local notebooks use Aer or `StatevectorSampler` and need no account. To try
a real device, export a token in the environment; never hard-code it:

```bash
export QISKIT_IBM_TOKEN="..."
```

The guarded cell in notebook 4 only connects when that variable is set. You also
need `qiskit-ibm-runtime` installed separately (for example
`uv add --project week-4 qiskit-ibm-runtime`) if you want to run it.

## Composer-era warning

The Week 4 video shows the 2018-era IBM Q Experience / Composer and a device
where `CNOT q2→q3` was not allowed. Today's Composer UI is different, and the
Qiskit transpiler routes and flips CNOTs automatically. Answer course questions
using the course framing; expect a different UI when doing the lab.

## Dependencies

Declared in `pyproject.toml`:

- `qiskit` and `qiskit-aer` for local simulation
- `numpy` and `matplotlib` for statevector work and histograms
- `jupyterlab` and `ipykernel` for the notebooks
- `pytest` (dev group) for `qasm-check` acceptance tests

`uv.lock` pins the resolved environment for reproducibility.
