#!/usr/bin/env python3
"""Computational-basis states |0> and |1>.

Prepare both basis states, inspect their statevectors, measure them,
and show that measurement collapses the state with certainty.
"""

from __future__ import annotations

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def build_zero_state() -> Circuit:
    """Return an empty circuit — qubit starts in |0>."""
    return Circuit()


def build_one_state() -> Circuit:
    """Return a circuit that flips to |1> with X."""
    circuit = Circuit()
    circuit.x(0)
    return circuit


def build_superposition() -> Circuit:
    """Return H|0> for contrast (50/50, not a basis state)."""
    circuit = Circuit()
    circuit.h(0)
    return circuit


def demo_zero_state() -> None:
    """Show the |0> state: default qubit after init."""
    print("=== |0> state (qubit default) ===")
    circuit = build_zero_state()
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    state_vector = result.result_types[0].value
    probabilities = result.result_types[1].value
    print(f"state vector: {state_vector}")
    print(f"probabilities: {probabilities}")
    print()


def demo_one_state() -> None:
    """Show the |1> state: flip with X gate."""
    print("=== |1> state (X gate) ===")
    circuit = build_one_state()
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    state_vector = result.result_types[0].value
    probabilities = result.result_types[1].value
    print(f"state vector: {state_vector}")
    print(f"probabilities: {probabilities}")
    print()


def demo_superposition() -> None:
    """Show equal superposition via Hadamard for contrast."""
    print("=== (|0> + |1>)/sqrt(2) via Hadamard ===")
    circuit = build_superposition()
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    state_vector = result.result_types[0].value
    probabilities = result.result_types[1].value
    print(f"state vector: {state_vector}")
    print(f"probabilities: {probabilities}")
    print()


def main() -> None:
    demo_zero_state()
    demo_one_state()
    demo_superposition()


if __name__ == "__main__":
    main()
