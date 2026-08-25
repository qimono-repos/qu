# QU is Quantum for Qimono

### Get into Quantum programming with Microsoft and Azure

[Microsoft Quantum](https://quantum.microsoft.com/)

### Get started in Quantom programming using Q# in Azure
[Quantum Coding](https://quantum.microsoft.com/en-us/tools/quantum-coding)

![quantum-image](assets/quantum-image.png)

## Stacks

This is a **polyglot quantum computing playground**. Each framework lives
in its own folder with a standalone toolchain. All Python stacks use the
shared Guix manifest at the repo root.

| Stack | What it is | Where |
|---|---|---|
| **Q#** | Microsoft's standalone quantum language | [`qsharp/`](qsharp/) |
| **Qiskit** | IBM gate-model SDK | [`qiskit/`](qiskit/) |
| **Cirq** | Google gate-model SDK | [`cirq/`](cirq/) |
| **PennyLane** | Xanadu QML + differentiable QC | [`pennylane/`](pennylane/) |
| **pytket** | Quantinuum circuit compiler/optimizer | [`pytket/`](pytket/) |
| **D-Wave Ocean** | Quantum annealing toolkit | [`dwave-ocean/`](dwave-ocean/) |
| **Amazon Braket** | Multi-hardware access (IonQ, Rigetti, D-Wave) | [`amazon-braket/`](amazon-braket/) |
| **Bloqade** | QuEra neutral-atom computing | [`bloqade/`](bloqade/) |
| **PyQuil** | Rigetti Quil language | [`pyquil/`](pyquil/) |
| **CUDA-Q** | NVIDIA GPU-accelerated QC | [`cuda-q/`](cuda-q/) |
| **Stim** | Google error-correction | [`Stim/`](Stim/) |
| **QClojure** | Functional QC in Clojure | [`qclojure/`](qclojure/) |

## Topic tree

All gate-model frameworks share a canonical topic structure:

```
basic/            computational-basis, statevectors, logic-gates, phase,
                  superposition, bloch-sphere, measurement, tensor-products,
                  controlled-gates, entanglement, toffoli

algorithms/       oracle-basics, phase-kickback, deutsch-jozsa, qft,
                  phase-estimation, shor, grover

cryptography/     rsa, bb84, entanglement-qkd, qrng, teleportation
                  (Qiskit, PennyLane, Q#)

simulation/       hamiltonians, time-evolution, vqe
                  (Qiskit, PennyLane, Braket)

optimization/     qaoa, tsp, adiabatic
                  (Qiskit, PennyLane, D-Wave, QClojure, Q#)

machinelearning/  qml-classifier, qml-regression, quantum-kernel
                  (PennyLane, Qiskit)

error-correction/ stabilizer-codes, surface-codes, noise-models
                  (Stim)
```

## Shared topics

| Topic | Where |
|---|---|
| [`big-o/`](big-o/) | Root — O(1) and O(log n) in Q# and Clojure |
| [`utilities/python/visualization/`](utilities/python/visualization/) | Root — shared circuit/Bloch/distribution savers |

## Setup (Python stacks)

All Python stacks use the same pattern:

```bash
cd <stack>          # e.g., cd pennylane
guix shell -m ../manifest.scm
uv sync --python python3
exit
./run python <topic>/<script>.py
./run jupyter notebook
```

CUDA-Q is the exception — it runs natively on Ubuntu with NVIDIA GPU.
QClojure is the exception — it uses JVM + Leiningen (provided by Guix).

Full setup details: [`AGENTS.md`](AGENTS.md)

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
