#!/usr/bin/env python3
"""Statevector inspection with the |+> state.

Create the |+> state, inspect its statevector representation,
and show amplitudes, probabilities, and the full ket decomposition.
"""

from __future__ import annotations

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def demo_plus_state() -> None:
    """Build |+> = H|0> and inspect the statevector."""
    print("=== |+> = H|0> ===")
    circuit = Circuit()
    circuit.h(0)
    print(circuit)

    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    state_vector = result.result_types[0].value
    probabilities = result.result_types[1].value

    print(f"state vector: {state_vector}")
    print(f"probabilities: {probabilities}")
    print(f"norm: {sum(abs(a) ** 2 for a in state_vector):.6f}")
    print()


def demo_minus_state() -> None:
    """Build |-> = HX|0> and inspect."""
    print("=== |-> = HX|0> ===")
    circuit = Circuit()
    circuit.x(0)
    circuit.h(0)
    print(circuit)

    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    state_vector = result.result_types[0].value
    probabilities = result.result_types[1].value

    print(f"state vector: {state_vector}")
    print(f"probabilities: {probabilities}")
    print()


def demo_plus_i_state() -> None:
    """Build |+i> = HS|0> and inspect."""
    print("=== |+i> = HS|0> ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.s(0)
    print(circuit)

    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    state_vector = result.result_types[0].value
    probabilities = result.result_types[1].value

    print(f"state vector: {state_vector}")
    print(f"probabilities: {probabilities}")
    print()


def demo_two_qubit_tensor() -> None:
    """Show that tensor product of |+> with |0> gives a 4-element statevector."""
    print("=== tensor product |+> x |0> ===")
    circuit = Circuit()
    circuit.h(1)  # qubit 1 gets H, qubit 0 stays |0>
    print(circuit)

    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    state_vector = result.result_types[0].value
    probabilities = result.result_types[1].value

    print(f"state vector length: {len(state_vector)}")
    print(f"probabilities: {probabilities}")
    print()


def main() -> None:
    demo_plus_state()
    demo_minus_state()
    demo_plus_i_state()
    demo_two_qubit_tensor()


if __name__ == "__main__":
    main()
