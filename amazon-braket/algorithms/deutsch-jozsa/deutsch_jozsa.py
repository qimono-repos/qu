#!/usr/bin/env python3
"""Deutsch-Jozsa algorithm (n=2 bits).

Given a black-box function f : {0,1}^n -> {0,1} promised to be either
constant (all zeros or all ones) or balanced (exactly half zeros, half
ones), Deutsch-Jozsa determines which in a single query.

n=2: we test all 6 balanced functions and the 2 constant functions.
"""

from __future__ import annotations

from braket.circuits import Circuit
from braket.devices import LocalSimulator


def oracle_constant_0() -> Circuit:
    """f(x) = 0 for all x.  Does nothing — ancilla unchanged."""
    return Circuit()


def oracle_constant_1() -> Circuit:
    """f(x) = 1 for all x.  X on ancilla flips it unconditionally."""
    circuit = Circuit()
    circuit.x(2)
    return circuit


def oracle_balanced_id() -> Circuit:
    """f(x0,x1) = x0  (identity on first bit)."""
    circuit = Circuit()
    circuit.cnot(0, 2)
    return circuit


def oracle_balanced_not() -> Circuit:
    """f(x0,x1) = NOT x0."""
    circuit = Circuit()
    circuit.cnot(0, 2)
    circuit.x(2)
    return circuit


def oracle_balanced_xor() -> Circuit:
    """f(x0,x1) = x0 XOR x1."""
    circuit = Circuit()
    circuit.cnot(0, 2)
    circuit.cnot(1, 2)
    return circuit


def oracle_balanced_xnor() -> Circuit:
    """f(x0,x1) = NOT (x0 XOR x1)."""
    circuit = Circuit()
    circuit.cnot(0, 2)
    circuit.cnot(1, 2)
    circuit.x(2)
    return circuit


def oracle_balanced_msb() -> Circuit:
    """f(x0,x1) = x1."""
    circuit = Circuit()
    circuit.cnot(1, 2)
    return circuit


def oracle_balanced_nand() -> Circuit:
    """f(x0,x1) = NOT (x0 AND x1)."""
    circuit = Circuit()
    circuit.ccnot(0, 1, 2)
    circuit.x(2)
    return circuit


def deutsch_jozsa(oracle_fn, n: int = 2) -> Circuit:
    """Build the Deutsch-Jozsa circuit.

    Layout: qubits 0..n-1 are input, qubit n is ancilla.

    1. Ancilla to |->.
    2. Hadamard on all input qubits.
    3. Oracle (controlled-f).
    4. Hadamard on all input qubits.
    5. Measure input qubits.
    """
    circuit = Circuit()
    circuit.x(n)
    circuit.h(n)
    for i in range(n):
        circuit.h(i)

    circuit.add_circuit(oracle_fn())

    for i in range(n):
        circuit.h(i)
    for i in range(n):
        circuit.measure(i)
    return circuit


def run_dj(name: str, oracle_fn, n: int = 2) -> None:
    """Run Deutsch-Jozsa and classify the result."""
    circuit = deutsch_jozsa(oracle_fn, n)
    device = LocalSimulator()
    result = device.run(circuit, shots=100).result()
    counts = dict(result.measurement_counts)

    all_zeros = "0" * n
    is_constant = all(k == all_zeros for k in counts)
    verdict = "CONSTANT" if is_constant else "BALANCED"
    print(f"  {name:>20s}  counts={counts}  -> {verdict}")


def main() -> None:
    n = 2
    print(f"=== Deutsch-Jozsa (n={n}) ===")
    print("All-zero input measurement -> CONSTANT")
    print("Any non-zero input measurement -> BALANCED")
    print()

    oracles = [
        ("f=0 (constant)", oracle_constant_0),
        ("f=1 (constant)", oracle_constant_1),
        ("f=x0 (balanced)", oracle_balanced_id),
        ("f=NOT x0", oracle_balanced_not),
        ("f=x0 XOR x1", oracle_balanced_xor),
        ("f=NOT(x0 XOR x1)", oracle_balanced_xnor),
        ("f=x1 (balanced)", oracle_balanced_msb),
        ("f=NOT(x0 AND x1)", oracle_balanced_nand),
    ]

    for name, fn in oracles:
        run_dj(name, fn, n)

    print()
    print("All oracles classified correctly in ONE query.")
    print("Classical worst case requires 2^(n-1) + 1 queries.")


if __name__ == "__main__":
    main()
