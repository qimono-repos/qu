# CUDA-Q Workspace

NVIDIA CUDA-Q is a platform for hybrid quantum-classical computing. It lets
you write quantum kernels in Python (or C++) and run them on GPU-accelerated
simulators, with seamless CPU/GPU portability.

## GPU Requirements

- **Compute Capability 7.5+**: Turing (RTX 20xx), Ampere (A100, RTX 30xx),
  Ada Lovelace (RTX 40xx), Hopper (H100), Blackwell (B100/B200).
- Linux is the recommended platform. macOS supports CPU-only simulation.
  Windows works via WSL2.
- CUDA-Q runs on CPU without a GPU, but simulation speed is dramatically
  better with one.

## Setup on Ubuntu

```bash
# Verify GPU is visible
nvidia-smi

# Install CUDA Toolkit 12.x or 13.x
# https://developer.nvidia.com/cuda-downloads

# Install CUDA-Q
pip install cudaq

# For multi-GPU clusters, see the conda-based installer:
# https://nvidia.github.io/cuda-quantum/latest/using/install/local_installation.html
```

## Cloud Option

No local GPU? Use
[NVIDIA Quantum Cloud](https://www.nvidia.com/en-us/quantum-quantum-cloud/)
to run CUDA-Q workloads remotely.

## Workspace

| Topic | What it shows |
|---|---|
| `bell-state/` | Bell state with `@cudaq.kernel` + `cudaq.sample()` |
| `gpu-simulation/` | 20-qubit random circuit, GPU timing info |

Run any script:

```bash
python bell-state/bell_state.py
```

Execute a notebook with the installed kernel:

```bash
jupyter notebook  # select "Qimono Kernel CUDA-Q"
```
