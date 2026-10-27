# Quantum circuits in Clojure (Babashka)

`superposition-stats`: equal-superposition stats for n qubits (H^⊗n |0…0⟩). Runs on [Babashka](https://babashka.org); no JVM startup and no dependencies (plain Clojure vectors, `clojure.test` bundled with `bb`).

## Run

From this directory:

```bash
bb superposition-stats 4
bb test
```

Output:

```
n=4: summands=16, amplitude=0.250000, P per outcome=0.062500
```

## API

`(quantum-circuits.superposition/superposition-stats n)` returns `{:summands … :amplitude … :probability …}` and throws for n < 1.
The tests assert the 3-qubit (8, 1/√8, 1/8) and 4-qubit (16, 1/4, 1/16) cases.
