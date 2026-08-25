# D-Wave Ocean snippets

Quantum annealing takes a fundamentally different approach from gate-model
computing. Instead of building unitary circuits qubit by qubit, a quantum
annealer encodes the entire problem as an energy landscape and lets the
system evolve toward its lowest-energy state. The D-Wave hardware couples
hundreds or thousands of qubits in a Chimera or Pegasus graph and
physical annealing dynamics explore the solution space in parallel.

These snippets use **D-Wave Ocean SDK** with `neal.SimulatedAnnealingSampler`
for local simulation — no D-Wave Leap token or cloud access required.

## Setup

From the `dwave-ocean/` folder:

```bash
guix shell -m manifest.scm
uv sync --python python3
python -m ipykernel install --prefix=.venv --name=qimono-kernel-dwave \
    --display-name="Qimono Kernel D-Wave"
exit
```

Then run scripts with:

```bash
./run python basics/bqm-formulation/bqm_formulation.py
```

And notebooks with:

```bash
./run jupyter notebook
```

## Topics

```
basics/bqm-formulation    Binary Quadratic Model construction
basics/annealing-vs-gate  Simulated annealer vs Qiskit QAOA
problems/max-cut          MaxCut on C4 with Ocean
problems/tsp              4-city TSP as QUBO
```

## D-Wave Leap free tier

D-Wave offers a free **Leap** account that gives 1 minute of cloud QPU time
per month. Sign up at https://cloud.dwavesys.com/leap/ to submit problems
to real quantum hardware. Everything in this folder works locally without
an account — the simulated annealer produces identical sample sets for
small instances.
