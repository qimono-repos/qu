# QClojure — Functional Quantum Computing

[QClojure](https://github.com/lsolbach/qclojure) is a functional quantum
computing library for Clojure. It provides pure-functional circuit
construction, a comprehensive gate library, built-in algorithms (Grover,
QAOA, Shor, VQE, QFT, …), and an extensible simulator backend.

Clojure on the JVM is also a useful stepping stone toward future Kotlin
frontend work — same JVM, different language.

## Prerequisites

* **JVM 21+** (`java -version` should show 21 or later)
* **[Leiningen](https://leiningen.org/)** (`lein version`)

## Setup

```bash
lein deps
```

This fetches Clojure and all QClojure dependencies.

## Running

**REPL** (interactive exploration):

```bash
lein repl
```

Then load any example file:

```clojure
(load-file "examples/bell_state.clj")
```

**Scripts** (headless execution via `lein run` — each file is self-contained):

```bash
lein run -m examples.bell-state
```

Or run a single namespace directly:

```bash
lein run -m examples.grover
lein run -m examples.qaoa
lein run -m algorithms.grover
lein run -m algorithms.shor
```

## Examples

| File | What it does |
|---|---|
| `examples/bell_state.clj` | Creates a Bell state (H + CNOT), simulates, prints results |
| `examples/grover.clj` | Grover search on 3 qubits for state \|101⟩ |
| `examples/qaoa.clj` | MaxCut QAOA on a 4-vertex cycle graph |

## Algorithms

| File | What it does |
|---|---|
| `algorithms/oracle_basics/oracle_basics.clj` | Simple oracle marking \|11⟩ with a phase flip |
| `algorithms/phase_kickback/phase_kickback.clj` | Phase kickback mechanism via CZ gate |
| `algorithms/deutsch_jozsa/deutsch_jozsa.clj` | Deutsch-Jozsa algorithm (n=2), constant vs balanced |
| `algorithms/qft/qft.clj` | Quantum Fourier Transform on 3 qubits |
| `algorithms/phase_estimation/phase_estimation.clj` | QPE estimating phase π/4 with 3 precision qubits |
| `algorithms/shor/shor.clj` | Shor's algorithm factoring 15 = 3 × 5 |
| `algorithms/grover/grover.clj` | Grover search on 3 qubits for \|101⟩ |

## Optimization

| File | What it does |
|---|---|
| `optimization/qaoa/qaoa.clj` | QAOA for MaxCut on a 4-vertex cycle graph |
| `optimization/tsp/tsp.clj` | 4-city TSP as QUBO with penalty constraints |

## Useful links

* QClojure source: <https://github.com/lsolbach/qclojure>
* QClojure on Clojars: <https://clojars.org/org.soulspace/qclojure>
* cljdoc API docs: <https://cljdoc.org/d/org.soulspace/qclojure>
