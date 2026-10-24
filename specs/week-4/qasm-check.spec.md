# Spec: qasm-check

Status: draft v1 · Owner: Albert · Implementer: any (local LLM welcome) · Location for code: `tools/qasm-check/`

## 1. Goal

A small CLI that takes an OpenQASM file Albert wrote by hand (Composer export or text editor), simulates it locally with Qiskit, and tells him whether it does what he predicted. It is a **checker**, not a generator: it never writes circuits.

## 2. Non-goals

- No circuit generation, no "suggest a fix".
- No IBM cloud calls in v1 (real-device runs are done by hand in Composer / IBM Quantum).
- No GUI.

## 3. Environment

- Python 3.10+, Qiskit 1.x or 2.x (print the installed version on every run).
- `qiskit-aer` optional; fall back to `qiskit.primitives.StatevectorSampler` if Aer is missing.
- Runs offline.

## 4. Interface

```
qasm-check FILE.qasm [--expect EXPECT] [--shots N] [--seed S] [--statevector] [--draw] [--qasm3]
qasm-check equiv A.qasm B.qasm
```

- `FILE.qasm`: OpenQASM 2.0 by default (`include "qelib1.inc";`); `--qasm3` parses OpenQASM 3.
- `--expect`: expected measurement distribution, e.g. `"00:0.5,11:0.5"` or `"1:1.0"`. Keys are bitstrings in **Qiskit order (classical bit c[n-1] on the left, c[0] on the right)**.
- `--shots`: default 1024. `--seed`: default 42, so runs are reproducible.
- `--statevector`: remove final measurements and print the statevector with exact forms where recognizable (0.7071… → 1/√2, 0.5 → 1/2, phases as ±, ±i).
- `--draw`: print the text circuit diagram.
- `equiv`: drop final measurements from both files and report whether the two unitaries are equal up to global phase (`Operator.equiv`).

## 5. Output

1. Qiskit version, parsed file name, number of qubits and classical bits.
2. Circuit diagram (if `--draw`).
3. Counts sorted by bitstring, with probabilities.
4. If `--expect`: PASS or FAIL per outcome. Tolerance: expected p = 0 or 1 must be exact in the ideal simulation; otherwise |measured − expected| ≤ 3·sqrt(p(1−p)/shots).
5. A one-line reminder of the bit-order convention.

Exit code: 0 on PASS (or no expectation), 1 on FAIL, 2 on parse error. Parse errors print the line number and the parser message unchanged.

## 6. Acceptance tests (pytest, `tools/qasm-check/tests/`)

| # | Input | Expect |
|---|---|---|
| T1 | Bell: `h q[0]; cx q[0],q[1];` measure both | `00` and `11` near 0.5, PASS |
| T2 | `x q[0];` measure into `c[0]` of a 2-bit creg | counts key `01` (bit order check) |
| T3 | `h q[0]; z q[0]; h q[0];` measure | `1` with p = 1 exactly |
| T4 | `equiv` of `cx q[1],q[0];` vs `h q[0]; h q[1]; cx q[0],q[1]; h q[0]; h q[1];` | equal |
| T5 | File with a syntax error | exit 2, line number shown |
| T6 | `--statevector` on `h q[0];` | prints 1/√2 for both amplitudes |
| T7 | Same file, same seed, twice | identical counts |

## 7. Done when

All tests pass, `README.md` in `tools/qasm-check/` shows one example run, and the tool runs on Albert's local machine.

## 8. Out of scope until after the course

Real-device submission, noise models from IBM backends, OpenQASM 3 classical control flow.
