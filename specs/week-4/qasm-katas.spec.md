# Spec: OpenQASM katas (ungraded)

Status: draft v1 · Purpose: learn OpenQASM 2.0 syntax by writing small circuits by hand, predict, then check with `qasm-check`.

Rules:
- Albert writes every `.qasm` file himself, in `practice/week-4/katas/`.
- Write the prediction in the kata's log line **before** running.
- These are not the graded QASM questions or the graded lab. Nothing from the graded items goes here.

Every file starts with:

```
OPENQASM 2.0;
include "qelib1.inc";
```

| # | Kata | Concept | Check |
|---|---|---|---|
| K1 | One qubit, `measure` only | Default state, registers | `qasm-check k1.qasm --expect "0:1.0"` |
| K2 | `x`, then measure | Bit flip | expect `1:1.0` |
| K3 | `h`, then measure | Superposition, shots vs probabilities | expect `0:0.5,1:0.5` |
| K4 | `h; z; h` | Relative phase becomes measurable after H | write your own expect |
| K5 | `h; s; s; h` | Same idea, S·S = Z | `equiv` against K4 |
| K6 | 2 qubits, `x q[0]`, measure both | Bit order in counts strings | predict the string |
| K7 | Bell pair | Entanglement, correlations | expect `00`, `11` |
| K8 | Bell pair on hardware-style constraint: only `cx q[1],q[0]` allowed | CNOT flip with H sandwich | `equiv` against `cx q[0],q[1]` |
| K9 | 3-qubit GHZ | Chained CNOTs | write your own expect |
| K10 | `h` on 3 qubits, measure | Equal superposition, 1/8 each | expect 8 outcomes near 0.125 |
| K11 | Data qubit |0⟩, ancilla |1⟩, H on both, H on both again | Phase kickback setup without any oracle | predict both qubits |
| K12 | Export a Composer circuit to QASM and diff it with your hand-written one | Composer ↔ QASM | identical behaviour |

Log format (append to the week log, not here):

```
K4 · prediction: ___ · result: ___ · surprise: ___
```
