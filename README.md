# QU is Quantum for Qimono

### Get into Quantum programming with Microsoft and Azure

[Microsoft Quantum](https://quantum.microsoft.com/)

### Get started in Quantom programming using Q# in Azure
[Quantum Coding](https://quantum.microsoft.com/en-us/tools/quantum-coding)

![quantum-image](assets/quantum-image.png)

## Qiskit

The [`qiskit/`](qiskit/) folder is a standalone Python + Jupyter workspace
for IBM Qiskit. It is separate from the Q# / Cirq / Stim material: no
shared package, no cross-imports.

Toolchain on this Ubuntu host:

- **Python** and **uv** come from [Guix](https://guix.gnu.org/) (`qiskit/manifest.scm`)
- Qiskit 2.x, Aer, NumPy, SciPy, Matplotlib, and Jupyter are installed by `uv`

Each topic is its own folder with a `.py` script **and** a matching
`.ipynb`. Folder names are words only (no numbers).

| Folder | Topic |
|---|---|
| [`qiskit/basic/logic-gates`](qiskit/basic/logic-gates) | Pauli, H, S, T, CX, SWAP |
| [`qiskit/basic/superposition`](qiskit/basic/superposition) | Hadamard + CX, Bell pairs |
| [`qiskit/basic/toffoli`](qiskit/basic/toffoli) | Toffoli (CCX) |
| [`qiskit/algorithms/shor`](qiskit/algorithms/shor) | Shor period finding, factor 15 |
| [`qiskit/algorithms/grover`](qiskit/algorithms/grover) | Grover search |
| [`qiskit/hybrid/qaoa`](qiskit/hybrid/qaoa) | QAOA MaxCut |
| [`qiskit/hybrid/tsp`](qiskit/hybrid/tsp) | Traveling salesperson |
| [`qiskit/hybrid/quantum-machine-learning`](qiskit/hybrid/quantum-machine-learning) | Hybrid variational classifier |

Setup and run commands live in [`qiskit/README.md`](qiskit/README.md).
Short version:

```bash
cd qiskit
guix shell -m manifest.scm
uv sync --python python3
source env.sh
./run python basic/logic-gates/logic_gates.py
./run jupyter notebook
```

## Agents

Coding-agent instructions live in [`agents/`](agents/). That folder is
the result of collecting the per-tool guides in one place:

| File | Who it is for |
|---|---|
| [`agents/AGENTS.md`](agents/AGENTS.md) | Shared agent README (Grok and any tool that reads the [AGENTS.md](https://agents.md/) format) |
| [`agents/GEMINI.md`](agents/GEMINI.md) | Gemini CLI / Google Gemini (moved here from the repo root, then updated with the Qiskit subproject) |
| [`agents/copilot-instructions.md`](agents/copilot-instructions.md) | GitHub Copilot Chat / Edits |

Root [`AGENTS.md`](AGENTS.md) and [`GEMINI.md`](GEMINI.md) are
symlinks into `agents/`, so tools that only look at the repository root
still load the same files.
