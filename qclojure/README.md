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
```

## Examples

| File | What it does |
|---|---|
| `examples/bell_state.clj` | Creates a Bell state (H + CNOT), simulates, prints results |
| `examples/grover.clj` | Grover search on 3 qubits for state \|101⟩ |
| `examples/qaoa.clj` | MaxCut QAOA on a 4-vertex cycle graph |

## Useful links

* QClojure source: <https://github.com/lsolbach/qclojure>
* QClojure on Clojars: <https://clojars.org/org.soulspace/qclojure>
* cljdoc API docs: <https://cljdoc.org/d/org.soulspace/qclojure>
