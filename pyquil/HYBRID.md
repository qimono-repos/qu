# Hybrid classical-quantum approach

PyQuil supports **hybrid quantum-classical workflows** where Quil programs
are compiled by `quilc` and executed on QVM with classical post-processing.

## When to use hybrid

| Problem type | Classical role | Quantum role | Example |
|---|---|---|---|
| Variational algorithms | Optimize parameters | Execute Quil program | VQE, QAOA |
| Error mitigation | Readout correction | Noisy measurements | DET, PCR |
| Circuit compilation | Optimize gate sequence | Execute compiled circuit | quilc pipeline |

## PyQuil hybrid examples

- `basics/bell-state/` — Bell state preparation and measurement
- `circuits/parameterized/` — Parameterized circuits for variational algorithms

## Key pattern

PyQuil's hybrid loop:

```
1. Classically generate Quil program with parameters
2. Compile via quilc (gate optimization)
3. Execute on QVM (simulator) or QPU (hardware)
4. Process measurement results
5. Update parameters, repeat
```
