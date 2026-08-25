# PennyLane workspace

Standalone PennyLane snippets covering quantum-classical interop, QML
gradients, and number-theory demos. Every topic is its own folder with
a `.py` script and a matching Jupyter notebook. Nothing is imported
across folders.

## Setup

From **this directory** (`pennylane/`, next to `pyproject.toml`):

```bash
guix shell -m manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-pennylane \
    --display-name="Qimono Kernel PennyLane"
exit
```

Run scripts with `./run` so the Guix profile is on `LD_LIBRARY_PATH`:

```bash
./run python qiskit-compatibility/bell-states/bell_states.py
```

## Layout

```
qiskit-compatibility/
  bell-states/            Bell state via PennyLane (H + CNOT)
  grover-search/          Grover search for |101⟩ on 3 qubits
  qft/                    Quantum Fourier Transform, 4 qubits
  qaoa-max-cut/           QAOA MaxCut on C4
features/
  gradients/              parameter-shift, backprop, adjoint comparison
  qml-classifier/         variational XOR classifier
  qml-regression/         continuous QNN for sine regression
number-theory/
  order-finding/          period finding via QFT (core of Shor)
  prime-identification/   VQE-style prime identification
```

## Notebooks

```bash
./run jupyter notebook
```

Each notebook is self-contained (no import of the sibling `.py` file)
and uses the **Qimono Kernel PennyLane** kernel.
