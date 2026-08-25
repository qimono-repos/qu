# Bloqade — Quantum for Qimono

[Bloqade](https://bloqade.quera.com/) is QuEra's Python SDK for
neutral-atom quantum computing. It targets QuEra's Aquila QPU (up to
256 qubits) and a local emulator for development.

## Two paradigms

### Analog mode

Atoms are placed in a 1D or 2D array and driven with global laser
pulses. The native Hamiltonian is the Rydberg blockade Hamiltonian —
no gate decomposition needed. You control atom positions, Rabi
frequency Ω(t), detuning Δ(t), and the interaction radius Rb. This is
natural for simulation tasks (Ising models, optimization, phase
transitions).

### Digital mode

The SQUIN DSL lets you write gate-based circuits with a
`@squin.kernel` decorator, mid-circuit measurement, and classical
feed-forward. Under the hood, Bloqade compiles SQUIN programs to
Rydberg pulse sequences. If the SQUIN runtime is not yet available,
you can build circuits in Cirq and import them via
`bloqade.circuit.load_circuit`.

## Early-stage warning

Bloqade is under active development. APIs, class names, and module
paths may change between releases. The code in this workspace targets
`bloqade >= 0.15` and follows the API as of mid-2025. If imports
break, check the [Bloqade docs](https://bloqade.quera.com/) for
migration notes.

## Setup (Guix + uv)

```bash
guix shell -m manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-bloqade \
    --display-name="Qimono Kernel Bloqade"
exit
```

Run scripts with `./run`:

```bash
./run python analog/rydberg-atom-chain/rydberg_atom_chain.py
```

Notebooks use kernel **Qimono Kernel Bloqade**.

## Workspace layout

```
bloqade/
├── README.md
├── requirements.txt
├── pyproject.toml
├── run                          # wrapper (do not source)
├── env.sh                       # Guix shell env (do not source interactively)
├── analog/
│   ├── rydberg-atom-chain/      1D Rydberg chain, Rabi sweep
│   └── parameter-sweep/         Sweep spacing → ordered/disordered phases
└── digital/
    └── squin-circuits/          GHZ via SQUIN or Cirq interop
```

All examples run **locally by default**. No QPU access is required.
