# GitHub Copilot instructions

Workspace instructions for Copilot Chat / Copilot Edits in **qu**
(Quantum for Qimono). Prefer [`AGENTS.md`](AGENTS.md) when a rule here
and a rule there disagree.

## What this repo is

A personal quantum-learning repo. Several stacks, one tree:

- Q# + C# (`TrainingQsharp/`, `teleportation.qs`) — .NET 8, Quantum SDK 0.28
- Qiskit snippets (`qiskit/`) — Guix Python + uv, Qiskit 2.x + Aer
- Cirq demos at the repo root
- Stim under `Stim/`

Do not turn this into a shared Python package or a monorepo build.

## When editing Qiskit

- Keep each topic **standalone**. No cross-folder imports.
- Ship **both** `*.py` and `*.ipynb`. The notebook must not import the script.
- Folder names: words and hyphens only (`basic/logic-gates`, `hybrid/qaoa`).
- Use Qiskit 2 APIs. No `QuantumInstance`, no `qiskit.Aer`.
- `expectation_value` takes `SparsePauliOp` / `Pauli`, not a plain string.
- Qubit 0 is the **rightmost** bit in printed bitstrings.
- Run via `qiskit/run` (Guix + `env.sh`). Do not `pip install` on Ubuntu system Python.
- Stay on tiny demos: Shor factors 15, Grover 3 qubits, TSP 4 cities.

## When editing Q#

- Target `net8.0` and `Microsoft.Quantum.Sdk`.
- Use operations + namespaces. Leave `@EntryPoint()` on the runnable op.
- Do not rename `porgram.cs`.

## Git

- Commit on `main`. No feature branches unless the user asks.
- Do not push unless asked.
- Conventional subjects: `feat:`, `docs:`, `fix:`.

## Do not

- Add IBM / Azure secrets.
- Commit `.venv/` or notebook checkpoints.
- Refactor unrelated historical files to "clean them up".
