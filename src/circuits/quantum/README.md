# Quantum circuits

Small terminal utilities for the Week 4 quantum circuit-model lesson (initialize → compute → measure).

## `superposition-stats`

Applies a Hadamard to each of n qubits starting in |0…0⟩ and reports the resulting **equal superposition**:

| n | summands (2ⁿ) | amplitude (normalizing coefficient) | probability per outcome |
|---|---|---|---|
| 3 | 8 | 1/√8 ≈ 0.353553 | 1/8 |
| 4 | 16 | 1/4 | 1/16 |

Rule: H^⊗n |0…0⟩ = (1/√2)ⁿ Σₓ |x⟩, so there are 2ⁿ summands, the amplitude is 1/√(2ⁿ), and each outcome has probability 1/2ⁿ. The amplitude and the probability are different numbers: the probability is the amplitude squared.

Both implementations build the n-qubit Hadamard as a Kronecker product H ⊗ H ⊗ … and read its first column. They check that all amplitudes are equal and that the squared magnitudes sum to 1.

## Projects

- [Python (`uv`, numpy)](python/README.md)
- [Clojure (Babashka, no dependencies)](babashka/README.md)
