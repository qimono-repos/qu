#!/usr/bin/env python3
"""Entanglement: Bell states and qubit correlations.

Create the Bell state |Phi+> = (|00> + |11>)/sqrt(2), show the
correlations between qubits, and verify with shot statistics.
"""

from __future__ import annotations

import json

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def bell_circuit() -> Circuit:
    """Build the Bell state |Phi+> = (|00> + |11>)/sqrt(2)."""
    circuit = Circuit()
    circuit.h(0)
    circuit.cnot(0, 1)
    return circuit


def demo_bell_state() -> None:
    """Create and inspect the Bell state."""
    print("=== Bell state |Phi+> = (|00> + |11>)/sqrt(2) ===")
    circuit = bell_circuit()
    print(circuit)

    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    amps = result.result_types[0].value
    probs = result.result_types[1].value

    print(f"amplitudes: {amps}")
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print()


def demo_correlations() -> None:
    """Show that qubit measurements are perfectly correlated."""
    print("=== Perfect correlations in Bell state ===")
    circuit = bell_circuit()
    measured = Circuit()
    measured.add_circuit(circuit)
    measured.measure(0)
    measured.measure(1)
    device = LocalSimulator()
    result = device.run(measured, shots=4000).result()
    counts = result.result_types[0].value
    print(f"counts: {counts}")
    agree = counts.get("00", 0) + counts.get("11", 0)
    print(f"Only |00> and |11> appear — qubits always agree.")
    print(f"  fraction same: {agree / 4000:.1%}")
    print()


def demo_measure_qubit0() -> None:
    """Measure only qubit 0 — qubit 1 still collapses."""
    print("=== Measure qubit 0 only, then inspect qubit 1 ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.cnot(0, 1)
    circuit.measure(0)
    device = LocalSimulator()
    result = device.run(circuit, shots=2000).result()
    counts = result.result_types[0].value
    print(f"counts (qubit 0 measured): {counts}")
    print("After measuring qubit 0, qubit 1 is always the same value.")
    print()


def demo_bell_states_gallery() -> None:
    """Show all four Bell states."""
    bell_states = {
        "|Phi+>": lambda: _bell(swap=False, phase_x=True),
        "|Phi->": lambda: _bell(swap=False, phase_x=False),
        "|Psi+>": lambda: _bell(swap=True, phase_x=True),
        "|Psi->": lambda: _bell(swap=True, phase_x=False),
    }

    device = LocalSimulator()
    print("=== Four Bell states ===")
    for name, make in bell_states.items():
        circuit = make()
        result = device.run(circuit, shots=0).result()
        probs = result.result_types[1].value
        print(f"{name}:")
        for state, prob in sorted(probs.items()):
            if prob > 1e-10:
                print(f"  |{state}> = {prob:.4f}")
        print()


def _bell(swap: bool = False, phase_x: bool = True) -> Circuit:
    """Helper to build a Bell state variant."""
    circuit = Circuit()
    if phase_x:
        circuit.x(0)
    circuit.h(0)
    circuit.cnot(0, 1)
    if swap:
        circuit.x(1)
    return circuit


def main() -> None:
    demo_bell_state()
    demo_correlations()
    demo_measure_qubit0()
    demo_bell_states_gallery()


if __name__ == "__main__":
    main()
