# Stim workspace

Quantum error correction experiments using Google's **Stim** stabilizer circuit
simulator.

## What is Stim?

Stim is a fast simulator for quantum error correction circuits that focuses on
stabilizer circuits and surface codes. It can efficiently simulate large error
correction codes that would be intractable with statevector simulators.

## Setup

From the `Stim/` folder:

```bash
guix shell -m manifest.scm
uv sync --python python3
exit
```

Then run scripts with:

```bash
./run python error-correction/stabilizer-codes/stabilizer_codes.py
```

## Topics

```
error-correction/stabilizer-codes  3-qubit bit-flip and phase-flip codes
error-correction/surface-codes     Distance-3 surface code (repetition code)
error-correction/noise-models      Depolarizing noise, threshold behavior
```

## Key concepts

- **Stabilizer codes**: Encode logical qubits into multiple physical qubits,
  detect errors via syndrome measurement
- **Surface codes**: 2D lattice of qubits with local stabilizer measurements,
  leading candidate for fault-tolerant quantum computing
- **Noise models**: How errors propagate through circuits and how error
  correction codes suppress them
