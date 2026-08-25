# Big-O in Quantum Computing

Examples of algorithmic complexity in quantum programs.

## Complexity classes

| Class | Quantum example | Notes |
|---|---|---|
| O(1) | Single-qubit measurement | Constant time, no dependence on input size |
| O(log n) | Grover's search | Quadratic speedup over classical O(n) |
| O(n) | Quantum Fourier Transform | Linear in qubit count |
| O(n³) | Shor's factoring | Polynomial speedup over classical exponential |

## Files

| File | Language | Topics |
|---|---|---|
| `csharp/BigO.qs` | Q# | O(1) measurement, O(log n) Grover on 3 qubits |
| `clojure/big_o.clj` | Clojure (QClojure) | O(1) measurement, O(log n) Grover on 3 qubits |

## Running

```bash
# Q#
qsharp run big-o/csharp/BigO.qs

# Clojure
cd big-o/clojure && lein repl
user=> (load-file "big_o.clj")
```
