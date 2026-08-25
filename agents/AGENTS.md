# AGENTS.md

This is the agent README for **qu** (Quantum for Qimono). Humans start at
the root [`README.md`](../README.md). Agents start here.

Sibling files in this folder:

- [`GEMINI.md`](GEMINI.md) — Gemini CLI / Google Gemini conventions
- [`copilot-instructions.md`](copilot-instructions.md) — GitHub Copilot

## Project overview

`qu` is a single-contributor playground for learning quantum programming.
It is a **polyglot repo**, not a library: Q#, Qiskit, Cirq, PennyLane,
D-Wave, Braket, Bloqade, PyQuil, CUDA-Q, Stim, and even Clojure live
side by side and do **not** share a build.

| Area | Stack | Where |
|---|---|---|
| Q# / Azure Quantum | Standalone Q# (modern syntax) | `qsharp/` |
| Qiskit | IBM gate-model, `.py` + `.ipynb` | `qiskit/` |
| Cirq | Google gate-model, `.py` + `.ipynb` | `cirq/` |
| PennyLane | Xanadu QML + differentiable QC, `.py` + `.ipynb` | `pennylane/` |
| pytket | Quantinuum circuit compiler, `.py` + `.ipynb` | `pytket/` |
| D-Wave Ocean | Quantum annealing, `.py` + `.ipynb` | `dwave-ocean/` |
| Amazon Braket | Multi-hardware access, `.py` + `.ipynb` | `amazon-braket/` |
| Bloqade | QuEra neutral atoms, `.py` + `.ipynb` | `bloqade/` |
| PyQuil | Rigetti Quil language, `.py` + `.ipynb` | `pyquil/` |
| CUDA-Q | NVIDIA GPU-accelerated QC, `.py` + `.ipynb` | `cuda-q/` |
| Stim | Google error-correction | `Stim/` |
| QClojure | Functional QC in Clojure, `.clj` | `qclojure/` |

Host: Ubuntu laptop with **Guix** (plus a GPU box for CUDA-Q).
There are no other contributors right now — **commit directly on `main`**.
Do not open feature branches or PRs unless the user asks.

## Shared Guix manifest

All Python workspaces share a single Guix manifest at the repo root:

```bash
guix shell -m manifest.scm
```

Per-workspace `manifest.scm` files are **symlinks** to `../manifest.scm`.
The manifest provides: `python`, `uv`, `gcc-toolchain`, `pkg-config`,
`openssl`, `zlib`, `openjdk21`, `leiningen`, `rust`, `cargo`.

CUDA-Q is the exception — it runs natively on Ubuntu with NVIDIA drivers,
not through Guix.

## Budget

Cloud service costs are documented in [`BUDGET.md`](BUDGET.md).

## Setup commands

### Q# (standalone, modern)

Modern Q# is a standalone compiler — no `.csproj` or C# host needed.

```bash
pip install qsharp
qsharp run qsharp/main.qs
```

For .NET 10 SDK (resource estimation, Azure Quantum):

```bash
# Flatpak (preferred)
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.microsoft.dotnet.Extension.Sdk

# Or Microsoft install script
wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh
chmod +x dotnet-install.sh
./dotnet-install.sh --channel 10.0 --install-dir $HOME/.dotnet
```

Full docs: [`qsharp/README.md`](../qsharp/README.md).

### Qiskit (Guix Python + uv)

From `qiskit/`:

```bash
guix shell -m ../manifest.scm
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
guix shell -m ../manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-cirq \
    --display-name="Qimono Kernel UV Cirq"
exit
```

Same Guix + uv rules as the Qiskit workspace: run scripts with
`./run python cirq-demo.py`, notebooks use kernel `qimono-kernel-cirq`.
Newer Cirq splits `cirq.google` into the separate `cirq_google`
package; the demo script falls back automatically.

### PennyLane (Guix Python + uv)

From `pennylane/`:

```bash
guix shell -m ../manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-pennylane \
    --display-name="Qimono Kernel PennyLane"
exit
```

Same Guix + uv rules: `./run python features/gradients/gradients.py`,
notebooks use kernel `qimono-kernel-pennylane`.

Full human docs: [`pennylane/README.md`](../pennylane/README.md).

### pytket (Guix Python + uv)

From `pytket/`:

```bash
guix shell -m ../manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-pytket \
    --display-name="Qimono Kernel pytket"
exit
```

Same rules: `./run python standalone/native-circuits/native_circuits.py`,
notebooks use kernel `qimono-kernel-pytket`.

Full human docs: [`pytket/README.md`](../pytket/README.md).

### D-Wave Ocean (Guix Python + uv)

From `dwave-ocean/`:

```bash
guix shell -m ../manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-dwave \
    --display-name="Qimono Kernel D-Wave"
exit
```

All examples use `neal.SimulatedAnnealingSampler` (local simulation,
no D-Wave API token needed).

Full human docs: [`dwave-ocean/README.md`](../dwave-ocean/README.md).

### Amazon Braket (Guix Python + uv)

From `amazon-braket/`:

```bash
guix shell -m ../manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-braket \
    --display-name="Qimono Kernel Braket"
exit
```

All examples use `LocalSimulator()` — no AWS credentials needed.
Full human docs: [`amazon-braket/README.md`](../amazon-braket/README.md).

### Bloqade (Guix Python + uv)

From `bloqade/`:

```bash
guix shell -m ../manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-bloqade \
    --display-name="Qimono Kernel Bloqade"
exit
```

Same rules: `./run python analog/rydberg-atom-chain/rydberg_atom_chain.py`,
notebooks use kernel `qimono-kernel-bloqade`. All examples use the local
emulator — no QPU access needed.

Full human docs: [`bloqade/README.md`](../bloqade/README.md).

### PyQuil (Guix Python + uv)

From `pyquil/`:

```bash
guix shell -m ../manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-pyquil \
    --display-name="Qimono Kernel PyQuil"
exit
```

Requires `quilc` and `QVM` servers running for full functionality.
See [`pyquil/README.md`](../pyquil/README.md) for Docker setup.

### CUDA-Q (native Ubuntu, not Guix)

From `cuda-q/`:

```bash
# Requires NVIDIA GPU (Compute Capability 7.5+) + CUDA toolkit
pip install cudaq
python cuda-q/bell-state/bell_state.py
```

See [`cuda-q/README.md`](../cuda-q/README.md) for full GPU setup.

### QClojure (JVM + Leiningen)

From `qclojure/`:

```bash
lein deps
lein repl
user=> (load-file "examples/bell_state.clj")
```

Requires JVM 21+ and Leiningen (both provided by shared Guix manifest).

Full docs: [`qclojure/README.md`](../qclojure/README.md).

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

- Target **Qiskit 2.x** (`qiskit>=2.0`, currently 2.5) + `qiskit-aer`.
  Do not use deprecated `QuantumInstance` or `qiskit.Aer`.
- `Statevector.expectation_value` needs a `SparsePauliOp` / `Pauli`,
  not a raw string.
- Qiskit bitstrings are **little-endian**: qubit 0 is the rightmost bit.
- Prefer local Aer / `Statevector`. Do not require an IBM Quantum token.
- Keep instances tiny (Shor factors 15, Grover N=8, TSP 4 cities).
- `.venv/` stays untracked. Commit `qiskit/uv.lock`.

## PennyLane subproject rules

- Same standalone rules: each topic self-contained, no cross-folder
  imports, every topic has a `.py` and sibling `.ipynb`.
- Folder names: hyphenated, words only, no numbers.
- Current topics:

  ```
  pennylane/qiskit-compatibility/bell-states
  pennylane/qiskit-compatibility/grover-search
  pennylane/qiskit-compatibility/qft
  pennylane/qiskit-compatibility/qaoa-max-cut
  pennylane/features/gradients
  pennylane/features/qml-classifier
  pennylane/features/qml-regression
  pennylane/number-theory/order-finding
  pennylane/number-theory/prime-identification
  ```

- Use `import pennylane as qml` (modern v0.45+ convention).
- PennyLane's `qml.QNode` uses `diff_method` for gradient computation.
- Prefer local simulation (`default.qubit` device).
- Keep instances tiny (2–4 qubits).
- `.venv/` stays untracked. Commit `pennylane/uv.lock` once created.

## pytket subproject rules

- Same standalone rules: each topic self-contained, every topic has a
  `.py` and sibling `.ipynb`.
- Folder names: hyphenated, words only, no numbers.
- Current topics:

  ```
  pytket/optimization-qiskit/circuit-optimize
  pytket/optimization-pennylane/circuit-optimize
  pytket/standalone/native-circuits
  ```

- pytket is a **circuit compiler/optimizer**, not a simulator.
- Use `from pytket import Circuit` for native circuits.
- Use `from pytket.qiskit import tk_to_qiskit, qiskit_to_tk` for interop.
- Show gate count reduction before/after optimization.
- Keep circuits small (2–4 qubits).
- `.venv/` stays untracked. Commit `pytket/uv.lock` once created.

## D-Wave Ocean subproject rules

- Same standalone rules: each topic self-contained, every topic has a
  `.py` and sibling `.ipynb`.
- Folder names: hyphenated, words only, no numbers.
- Current topics:

  ```
  dwave-ocean/basics/bqm-formulation
  dwave-ocean/basics/annealing-vs-gate
  dwave-ocean/problems/max-cut
  dwave-ocean/problems/tsp
  ```

- All examples use `neal.SimulatedAnnealingSampler` — no D-Wave token.
- Use `dimod.BinaryQuadraticModel` for BQM construction.
- Keep instances tiny (4 nodes/cities).
- `.venv/` stays untracked. Commit `dwave-ocean/uv.lock` once created.

## Amazon Braket subproject rules

- Same standalone rules: each topic self-contained, every topic has a
  `.py` and sibling `.ipynb`.
- Folder names: hyphenated, words only, no numbers.
- Current topics:

  ```
  amazon-braket/local-simulators/bell-state
  amazon-braket/local-simulators/ghz-state
  amazon-braket/hybrid/variational
  ```

- ALL examples use `LocalSimulator()` — no AWS credentials required.
- Use `from braket.circuit import Circuit` and
  `from braket.devices import LocalSimulator`.
- Keep circuits small (2–4 qubits).
- `.venv/` stays untracked. Commit `amazon-braket/uv.lock` once created.

## Bloqade subproject rules

- Same standalone rules: each topic self-contained, every topic has a
  `.py` and sibling `.ipynb`.
- Folder names: hyphenated, words only, no numbers.
- Current topics:

  ```
  bloqade/analog/rydberg-atom-chain
  bloqade/analog/parameter-sweep
  bloqade/digital/squin-circuits
  ```

- Bloqade is early-stage — APIs may change between releases. Write code
  to the correct API and note instability in the README.
- If SQUIN imports fail, fall back to Cirq interop via
  `bloqade.circuit.load_circuit`.
- Keep instances small (2–4 atoms/qubits).
- `.venv/` stays untracked. Commit `bloqade/uv.lock` once created.

## PyQuil subproject rules

- Same standalone rules: each topic self-contained, every topic has a
  `.py` and sibling `.ipynb`.
- Folder names: hyphenated, words only, no numbers.
- Current topics:

  ```
  pyquil/basics/bell-state
  pyquil/basics/ghz-state
  pyquil/circuits/parameterized
  ```

- Requires `quilc` (compiler) and `QVM` (simulator) servers running.
- Use `from pyquil import Program, get_qc` and `from pyquil.gates import *`.
- Keep circuits small (2–4 qubits).
- `.venv/` stays untracked. Commit `pyquil/uv.lock` once created.

## CUDA-Q subproject rules

- Same standalone rules: each topic self-contained, every topic has a
  `.py` and sibling `.ipynb`.
- Folder names: hyphenated, words only, no numbers.
- Current topics:

  ```
  cuda-q/bell-state
  cuda-q/gpu-simulation
  ```

- CUDA-Q runs **natively on Ubuntu** with NVIDIA GPU, not through Guix.
- Use `@cudaq.kernel` decorator and `cudaq.sample()`.
- GPU required for accelerated simulation; CPU fallback available.
- No `run` script or `env.sh` — run directly with `python`.
- Keep circuits small (2–20 qubits).

## QClojure subproject rules

- Clojure, not Python. No `.ipynb` files.
- Files live in `qclojure/examples/`.
- Current examples:

  ```
  qclojure/examples/bell_state.clj
  qclojure/examples/grover.clj
  qclojure/examples/qaoa.clj
  ```

- Requires JVM 21+ and Leiningen (both in shared Guix manifest).
- Run with `lein repl` then `(load-file "examples/bell_state.clj")`.
- Use QClojure API: `qclojure.quantum.*` namespace.

## Code style

- Match the file you are editing. Do not reformat unrelated code.
- Python: 4-space indent, type hints on new public functions, run under
  `if __name__ == "__main__":` for scripts.
- Notebooks: markdown for the idea, code cells self-contained, kernel
  name per workspace (see setup commands above).
- Q#: modern standalone syntax with `import Std.*` namespaces.
- Clojure: idiomatic Clojure (defn, let, threading macros).
- Do not "clean up" historical typos (`porgram.cs`, `Quantom` in the
  root README) unless the user asks.

## Testing instructions

There is no repo-wide test runner.

- Qiskit scripts: `qiskit/run python <path>` and confirm printed result.
- Qiskit notebooks: `jupyter nbconvert --execute --ExecutePreprocessor.kernel_name=qimono-kernel-python-3`.
- PennyLane scripts: `pennylane/run python <path>` and confirm printed result.
- PennyLane notebooks: `jupyter nbconvert --execute --ExecutePreprocessor.kernel_name=qimono-kernel-pennylane`.
- pytket scripts: `pytket/run python <path>` and confirm gate count reduction.
- D-Wave scripts: `dwave-ocean/run python <path>` and confirm optimization result.
- Amazon Braket scripts: `amazon-braket/run python <path>` and confirm printed result.
- Bloqade scripts: `bloqade/run python <path>` and confirm printed result.
- PyQuil scripts: `pyquil/run python <path>` (requires quilc + QVM running).
- CUDA-Q scripts: `python cuda-q/<path>` (requires NVIDIA GPU).
- QClojure: `cd qclojure && lein repl`, then load example files.
- Q#: `qsharp run qsharp/main.qs` prints simulator output.
- After any dependency change: `uv sync --python python3` in the
  affected workspace and re-run the touched scripts.

## Git and commits

- **Always commit on `main`.** No feature branches, no stacking, no PRs
  unless the user requests them.
- Conventional, present-tense subjects, matching history:
  `feat: …`, `docs: …`, `test: …`.
- Do not `git push` unless the user asks.
- Do not commit `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`.

## Security

- No cloud credentials are required for any snippets (all local simulation).
- Do not add IBM Quantum API keys, Azure Quantum connection strings,
  AWS access keys, D-Wave tokens, or secrets to the tree.
- Do not run destructive git commands (`reset --hard`, force-push)
  without asking.

## Pointers

- Human intro: [`README.md`](../README.md)
- Budget: [`BUDGET.md`](../BUDGET.md)
- Shared Guix manifest: [`manifest.scm`](../manifest.scm)
- Root requirements: [`requirements.txt`](../requirements.txt)
- Q# workspace: [`qsharp/README.md`](../qsharp/README.md)
- Qiskit how-to: [`qiskit/README.md`](../qiskit/README.md)
- Cirq how-to: [`cirq/README.md`](../cirq/README.md)
- PennyLane how-to: [`pennylane/README.md`](../pennylane/README.md)
- pytket how-to: [`pytket/README.md`](../pytket/README.md)
- D-Wave Ocean how-to: [`dwave-ocean/README.md`](../dwave-ocean/README.md)
- Amazon Braket how-to: [`amazon-braket/README.md`](../amazon-braket/README.md)
- Bloqade how-to: [`bloqade/README.md`](../bloqade/README.md)
- PyQuil how-to: [`pyquil/README.md`](../pyquil/README.md)
- CUDA-Q how-to: [`cuda-q/README.md`](../cuda-q/README.md)
- QClojure how-to: [`qclojure/README.md`](../qclojure/README.md)
- Microsoft Quantum: https://quantum.microsoft.com/
- Q# coding lab: https://quantum.microsoft.com/en-us/tools/quantum-coding
