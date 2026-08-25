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

## Qiskit

The [`qiskit/`](qiskit/) folder is a standalone Python + Jupyter workspace
for IBM Qiskit. It is separate from the Q# / Cirq / Stim material: no
shared package, no cross-imports.

| Folder | Topic |
|---|---|
| [`qiskit/basic/logic-gates`](qiskit/basic/logic-gates) | Pauli, H, S, T, CX, SWAP |
| [`qiskit/basic/superposition`](qiskit/basic/superposition) | Hadamard + CX, Bell pairs |
| [`qiskit/basic/toffoli`](qiskit/basic/toffoli) | Toffoli (CCX) |
| [`qiskit/big-o`](qiskit/big-o) | Classical Big O: $O(1)$ vs $O(\log n)$ |
| [`qiskit/algorithms/shor`](qiskit/algorithms/shor) | Shor period finding, factor 15 |
| [`qiskit/algorithms/grover`](qiskit/algorithms/grover) | Grover search |
| [`qiskit/algorithms/deutsch-jozsa`](qiskit/algorithms/deutsch-jozsa) | Deutsch–Jozsa, constant vs balanced |
| [`qiskit/hybrid/qaoa`](qiskit/hybrid/qaoa) | QAOA MaxCut |
| [`qiskit/hybrid/tsp`](qiskit/hybrid/tsp) | Traveling salesperson |
| [`qiskit/hybrid/quantum-machine-learning`](qiskit/hybrid/quantum-machine-learning) | Hybrid variational classifier |

## PennyLane

The [`pennylane/`](pennylane/) folder is a standalone Python + Jupyter
workspace for Xanadu PennyLane. Same Guix + uv toolchain as `qiskit/`.

| Folder | Topic |
|---|---|
| [`pennylane/qiskit-compatibility/bell-states`](pennylane/qiskit-compatibility/bell-states) | Bell states (PennyLane vs Qiskit) |
| [`pennylane/qiskit-compatibility/grover-search`](pennylane/qiskit-compatibility/grover-search) | Grover search |
| [`pennylane/qiskit-compatibility/qft`](pennylane/qiskit-compatibility/qft) | Quantum Fourier Transform |
| [`pennylane/qiskit-compatibility/qaoa-max-cut`](pennylane/qiskit-compatibility/qaoa-max-cut) | QAOA MaxCut |
| [`pennylane/features/gradients`](pennylane/features/gradients) | Gradient methods: parameter-shift, backprop, adjoint |
| [`pennylane/features/qml-classifier`](pennylane/features/qml-classifier) | Variational classifier (QML) |
| [`pennylane/features/qml-regression`](pennylane/features/qml-regression) | Continuous-output QNN |
| [`pennylane/number-theory/order-finding`](pennylane/number-theory/order-finding) | Quantum order finding (core of Shor) |
| [`pennylane/number-theory/prime-identification`](pennylane/number-theory/prime-identification) | VQE-style prime identification |

## Cirq

The [`cirq/`](cirq/) folder is a standalone Python + Jupyter workspace
for Google Cirq. It uses the same Guix + uv toolchain as `qiskit/`:
no shared package, no cross-imports.

| Folder | Topic |
|---|---|
| [`cirq/cirq-demo.ipynb`](cirq/cirq-demo.ipynb) | Explore `cirq.google` / `cirq_google` |
| [`cirq/cirq-fox.py`](cirq/cirq-fox.py) | Foxtail device grid |

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
