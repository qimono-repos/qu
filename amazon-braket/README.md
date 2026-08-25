# Amazon Braket — Quantum for Qimono

[Amazon Braket](https://aws.amazon.com/braket/) is a managed quantum
computing service that lets you run quantum circuits on hardware from
multiple providers — IonQ, QuEra, Rigetti, Oxford Quantum Circuits,
and others — through a single Python SDK. You write one
`braket.circuit.Circuit` and choose where to run it: a local simulator,
a managed cloud simulator, or a real quantum processing unit (QPU).

## Local simulators (free, no AWS account)

Every example in this workspace uses `LocalSimulator()`, which runs
entirely on your laptop. No AWS credentials or internet connection are
needed. This is the fastest way to learn Braket circuit construction
and验证 logic before spending money on cloud hardware.

## Moving to managed simulators and real QPUs

When you are ready to scale beyond local simulation:

1. **Create an AWS account** — follow the
   [Getting Started guide](https://aws.amazon.com/braket/getting-started/).
2. **Set credentials** — export `AWS_ACCESS_KEY_ID` and
   `AWS_SECRET_ACCESS_KEY`, or configure `~/.aws/credentials`.
3. **Switch the device** — replace `LocalSimulator()` with one of:

   | Device | Type | Best for |
   |--------|------|----------|
   | `SV1` | Statevector (managed) | Up to 34 qubits, fast statevector |
   | `DM1` | Density matrix (managed) | Noise modeling, up to 17 qubits |
   | `TN1` | Tensor network (managed) | Circuits with limited entanglement |
   | `IonQ Harmonic` | Trapped-ion QPU | High-fidelity, all-to-all connectivity |
   | `QuEra Aquila` | Neutral-atom QPU | Up to 256 qubits, analog mode |

   Example change:
   ```python
   from braket.aws import AwsDevice
   device = AwsDevice("arn:aws:braket:::device/qpu/ionq/Harmonic-1")
   ```

4. **Check pricing** — see the
   [Braket pricing page](https://aws.amazon.com/braket/pricing/) for
   per-shot and per-task costs.

## Setup (Guix + uv)

```bash
guix shell -m manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-braket \
    --display-name="Qimono Kernel Braket"
exit
```

Run scripts with `./run`:

```bash
./run python local-simulators/bell-state/bell_state.py
```

Notebooks use kernel **Qimono Kernel Braket**.

## Workspace layout

```
amazon-braket/
├── README.md
├── requirements.txt
├── pyproject.toml
├── run                          # wrapper (do not source)
├── env.sh                       # Guix shell env (do not source interactively)
├── local-simulators/
│   ├── bell-state/              Bell pair on LocalSVSimulator
│   └── ghz-state/               4-qubit GHZ on LocalSVSimulator
└── hybrid/
    └── variational/             VQE-style variational loop (local)
```

All examples run **locally by default**. No AWS account is required.
