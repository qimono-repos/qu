# AGENTS.md

This is the agent README for **qu** (Quantum for Qimono). Humans start at
the root [`README.md`](../README.md). Agents start here.

Sibling files in this folder:

- [`GEMINI.md`](GEMINI.md) — Gemini CLI / Google Gemini conventions
- [`copilot-instructions.md`](copilot-instructions.md) — GitHub Copilot

## Project overview

`qu` is a single-contributor playground for learning quantum programming.
It is a **polyglot repo**, not a library: Q#, Cirq, Stim, and Qiskit live
side by side and do **not** share a build.

| Area | Stack | Where |
|---|---|---|
| Q# / Azure Quantum | Q# + C# host, `Microsoft.Quantum.Sdk` 0.28, `net8.0` | `TrainingQsharp/`, `teleportation.qs`, `main.qs`, `porgram.cs` |
| Cirq | Python demos (Google Cirq, Foxtail device names) | `cirq/` |
| Stim | Error-correction experiments | `Stim/` |
| Qiskit | Standalone `.py` + `.ipynb` snippets | `qiskit/` |

Host: Ubuntu laptop with **Guix**. There are no other contributors right
now — **commit directly on `main`**. Do not open feature branches or PRs
unless the user asks.

## Setup commands

### Q# / .NET

```bash
dotnet build TrainingQsharp/TrainingQsharp.csproj
dotnet run --project TrainingQsharp/TrainingQsharp.csproj
```

The solution is `TrainingQsharp.sln`. The historical host file
`porgram.cs` (typo in the name) is part of the tree; do not "fix" the
filename unless asked.

### Qiskit (Guix Python + uv)

From `qiskit/`:

```bash
guix shell -m manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-python-3 \
    --display-name="Qimono Kernel UV Python"
exit
```

Guix Python does **not** search `/usr/lib`. Use `./run` so NumPy / Aer
see `libz` and `libstdc++`. Do **not** `source env.sh` in an interactive
shell (Ubuntu `ls` then dies with `GLIBC_2.43 not found`):

```bash
./run python basic/logic-gates/logic_gates.py
./run jupyter notebook
```

Do not install Qiskit with `pip` on the host Ubuntu Python. Do not
replace Guix Python with a `uv`-downloaded CPython unless the user asks.

Full human docs: [`qiskit/README.md`](../qiskit/README.md).

### Cirq (Guix Python + uv)

From `cirq/`:

```bash
guix shell -m manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-cirq \
    --display-name="Qimono Kernel UV Cirq"
exit
```

Same Guix + uv rules as the Qiskit workspace: run scripts with
`./run python cirq-demo.py`, notebooks use kernel `qimono-kernel-cirq`.
Newer Cirq splits `cirq.google` into the separate `cirq_google`
package; the demo script falls back automatically.

## Qiskit subproject rules

These are easy to get wrong. Follow them exactly.

- Each topic is a **standalone** program. Do not import helpers across
  `basic/`, `algorithms/`, or `hybrid/`.
- Every example exists as **both** a `.py` script and a sibling `.ipynb`.
  The notebook must not `import` the script.
- Folder names are words only, hyphenated, **no numbers**:
  `qiskit/basic/logic-gates`, `qiskit/hybrid/qaoa`.
- Current topics:

  ```
  qiskit/basic/logic-gates
  qiskit/basic/superposition      # Hadamard + CX / Bell
  qiskit/basic/toffoli
  qiskit/big-o                    # O(1) and O(log n) gallery
  qiskit/algorithms/shor          # factor 15
  qiskit/algorithms/grover        # search |101>
  qiskit/algorithms/deutsch-jozsa # constant vs balanced, n=2
  qiskit/hybrid/qaoa              # MaxCut on C4
  qiskit/hybrid/tsp               # 4-city traveling salesperson
  qiskit/hybrid/quantum-machine-learning
  ```

- Target **Qiskit 2.x** (`qiskit>=1.2`, currently 2.5) + `qiskit-aer`.
  Do not use deprecated `QuantumInstance` or `qiskit.Aer`.
- `Statevector.expectation_value` needs a `SparsePauliOp` / `Pauli`,
  not a raw string.
- Qiskit bitstrings are **little-endian**: qubit 0 is the rightmost bit.
- Prefer local Aer / `Statevector`. Do not require an IBM Quantum token.
- Keep instances tiny (Shor factors 15, Grover N=8, TSP 4 cities).
- `.venv/` stays untracked. Commit `qiskit/uv.lock`.

## Code style

- Match the file you are editing. Do not reformat unrelated code.
- Python: 4-space indent, type hints on new public functions, run under
  `if __name__ == "__main__":` for scripts.
- Notebooks: markdown for the idea, code cells self-contained, kernel
  `name` `qimono-kernel-python-3`, `display_name` "Qimono Kernel UV
  Python".
- Q#: namespaces + operations; `@EntryPoint()` marks the runnable
  operation. Target framework is `net8.0`.
- Do not "clean up" historical typos (`porgram.cs`, `Quantom` in the
  root README) unless the user asks.

## Testing instructions

There is no repo-wide test runner.

- Qiskit scripts: `qiskit/run python <path>` and confirm the printed
  result (Shor → `15 = 3 x 5`, Grover peaks on `|101>`, Deutsch–Jozsa
  constants give `|00>` / balanced does not, QAOA cut 4,
  TSP length 7, VQC accuracy 1.0 on XOR).
- Qiskit notebooks: execute with kernel `qimono-kernel-python-3`
  (`jupyter nbconvert --execute --ExecutePreprocessor.kernel_name=qimono-kernel-python-3`).
- Q#: `dotnet build` must succeed; `dotnet run` prints simulator output.
- After a Qiskit dependency change: `uv sync --python python3` and
  re-run the touched scripts.

## Git and commits

- **Always commit on `main`.** No feature branches, no stacking, no PRs
  unless the user requests them.
- `main` is often checked out in the primary clone
  (`/home/qi/source/repos/qimono-repos/qu`). This Grok worktree may be
  detached; after committing here, fast-forward that `main` checkout.
- Conventional, present-tense subjects, matching history:
  `feat: …`, `docs: …`, `test: …`.
- Do not `git push` unless the user asks.
- Do not commit `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`.

## Security

- No cloud credentials are required for the Qiskit snippets.
- Do not add IBM Quantum API keys, Azure Quantum connection strings, or
  secrets to the tree.
- Do not run destructive git commands (`reset --hard`, force-push)
  without asking.

## Pointers

- Human intro: [`README.md`](../README.md)
- Qiskit how-to: [`qiskit/README.md`](../qiskit/README.md)
- Qiskit Guix manifest: [`qiskit/manifest.scm`](../qiskit/manifest.scm)
- Q# project: [`TrainingQsharp/TrainingQsharp.csproj`](../TrainingQsharp/TrainingQsharp.csproj)
- Microsoft Quantum: https://quantum.microsoft.com/
- Q# coding lab: https://quantum.microsoft.com/en-us/tools/quantum-coding
