# GEMINI.md

Instructions for **Gemini CLI** and other Google Gemini coding agents
working in the `qu` repository. Canonical copy lives in `agents/`
(moved from the repo root). Cross-read [`AGENTS.md`](AGENTS.md) for the
shared project rules.

## Project Overview

`qu` (Quantum for Qimono) is a learning repo for quantum programming. It
is **not** a single application. Several stacks sit next to each other:

1. **Microsoft Quantum / Q#** — Q# algorithms with a C# host
   (`Microsoft.Quantum.Simulation`), originally the whole project.
2. **Qiskit** — standalone Python + Jupyter snippets under `qiskit/`.
3. **Cirq** — small Google Cirq demos at the repo root.
4. **Stim** — error-correction experiments in `Stim/`.

### Q# (original scope)

Key features:

- A "Quantum Hello World" that generates a random bit.
- Quantum teleportation of a qubit state.

Technologies:

- **Q#** for the quantum operations.
- **C#** host using `Microsoft.Quantum.Simulation`.
- **.NET 8** (`net8.0`), `Microsoft.Quantum.Sdk` 0.28.302812.

### Qiskit (new subproject)

`qiskit/` is a Guix + `uv` workspace. Python and `uv` come from Guix;
Qiskit 2.x, Aer, NumPy, SciPy, Matplotlib, and Jupyter come from `uv`.

Every topic is independent (no shared Python package). Each topic ships
**both** a `.py` file and a matching `.ipynb`. Folder names are words
only (no numbers), for example `qiskit/basic/logic-gates` and
`qiskit/hybrid/qaoa`.

| Folder | What it demonstrates |
|---|---|
| `qiskit/basic/logic-gates` | X, Y, Z, H, S, T, CX, SWAP |
| `qiskit/basic/superposition` | Hadamard + CX, Bell pairs |
| `qiskit/basic/toffoli` | CCX / reversible AND |
| `qiskit/algorithms/shor` | Period finding, factor 15 |
| `qiskit/algorithms/grover` | Grover search for `\|101>` |
| `qiskit/hybrid/qaoa` | QAOA MaxCut on a 4-cycle |
| `qiskit/hybrid/tsp` | 4-city traveling salesperson |
| `qiskit/hybrid/quantum-machine-learning` | Hybrid VQC on XOR |

Human setup: [`qiskit/README.md`](../qiskit/README.md).

## Building and Running

### Q#

You need the .NET SDK and the Microsoft Quantum Development Kit.

```bash
dotnet build
dotnet run --project TrainingQsharp/TrainingQsharp.csproj
```

The C# host (`porgram.cs` — historical filename) runs operations on the
full-state simulator and prints to the console.

### Qiskit

From `qiskit/`, on the Ubuntu + Guix host:

```bash
guix shell -m manifest.scm
uv sync --python python3
source env.sh
./run python basic/logic-gates/logic_gates.py
./run jupyter notebook
```

`env.sh` is required: Guix Python cannot see host `libz` / `libstdc++`,
which the uv wheels need. Prefer `./run` so that path is set for you.
Use the **Qiskit workspace** Jupyter kernel. No IBM Quantum token.

Expected smoke-test results:

- Shor: `15 = 3 x 5`
- Grover: histogram peaks on `|101>`
- QAOA: cut size 4 on C₄
- TSP: depot → harbor → market → tower, length 7
- VQC: accuracy 1.0 on the XOR table

## Development Conventions

- Q# lives in namespaces and operations; `@EntryPoint()` marks the
  runnable operation.
- Comments should explain the *quantum* idea, not restate the syntax.
- Qiskit examples must stay standalone: do not import across topic
  folders; do not have the notebook import the sibling `.py`.
- Write Qiskit 2.x code (`AerSimulator`, `SparsePauliOp`). Bitstrings
  print with qubit 0 on the **right**.
- Commit on `main` only. This repo has no branching strategy yet.
- Do not rename historical files (`porgram.cs`) unless asked.

## Related agent files

- [`AGENTS.md`](AGENTS.md) — shared, tool-agnostic agent README (Grok and others)
- [`copilot-instructions.md`](copilot-instructions.md) — GitHub Copilot
