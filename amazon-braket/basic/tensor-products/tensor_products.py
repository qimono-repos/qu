#!/usr/bin/env python3
"""Tensor products of quantum states.

Build multi-qubit systems by composing circuits and inspect the
resulting statevectors.  Show how |a> x |b> appears in the full
computational basis.
"""

from __future__ import annotations

import json

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def demo_zero_zero() -> None:
    """|0> tensor |0> = |00>."""
    print("=== |00> (default two-qubit state) ===")
    circuit = Circuit()
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    probs = result.result_types[1].value
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print()


def demo_one_zero() -> None:
    """X|0> tensor |0> = |10>."""
    print("=== |10> (X on qubit 1) ===")
    circuit = Circuit()
    circuit.x(1)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    probs = result.result_types[1].value
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print("Note: qubit 1 is leftmost in the bitstring, qubit 0 is rightmost.")
    print()


def demo_zero_one() -> None:
    """|0> tensor X|0> = |01>."""
    print("=== |01> (X on qubit 0) ===")
    circuit = Circuit()
    circuit.x(0)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    probs = result.result_types[1].value
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print()


def demo_one_one() -> None:
    """X tensor X = |11>."""
    print("=== |11> (X on both qubits) ===")
    circuit = Circuit()
    circuit.x(0)
    circuit.x(1)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    probs = result.result_types[1].value
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print()


def demo_superposition_tensor() -> None:
    """|+> tensor |0> = (|00> + |10>)/sqrt(2)."""
    print("=== |+> x |0> = (|00> + |10>)/sqrt(2) ===")
    circuit = Circuit()
    circuit.h(1)  # H on qubit 1 (left qubit in the diagram)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    probs = result.result_types[1].value
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print("The left qubit is in |+>, the right qubit is in |0>.")
    print()


def demo_both_superposition() -> None:
    """|+> tensor |+> = (|00> + |01> + |10> + |11>)/2."""
    print("=== |+> x |+> = (|00> + |01> + |10> + |11>)/2 ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.h(1)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    probs = result.result_types[1].value
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print("All four basis states equally likely — product of two 50/50 states.")
    print()


def main() -> None:
    demo_zero_zero()
    demo_one_zero()
    demo_zero_one()
    demo_one_one()
    demo_superposition_tensor()
    demo_both_superposition()


if __name__ == "__main__":
    main()
