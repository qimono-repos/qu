#!/usr/bin/env python3
"""Basic quantum logic gates as standalone Braket circuits.

Each gate is applied to a computational-basis input and simulated
exactly with the local statevector simulator. Nothing here is imported
from the other example folders.
"""

from __future__ import annotations

import json

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def run_statevector(circuit: Circuit) -> dict[str, float]:
    """Return the probabilities dict for a circuit (shots=0)."""
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    return result.result_types[1].value


def run_amplitudes(circuit: Circuit) -> list[complex]:
    """Return the statevector (amplitudes) for a circuit."""
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    return result.result_types[0].value


def demo_pauli_x() -> None:
    """Pauli-X (NOT) on |0> flips to |1>."""
    print("=== Pauli-X (NOT) on |0> ===")
    circuit = Circuit()
    circuit.x(0)
    print(circuit)
    probs = run_statevector(circuit)
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print()


def demo_pauli_y() -> None:
    """Pauli-Y on |0> gives i|1>."""
    print("=== Pauli-Y on |0> ===")
    circuit = Circuit()
    circuit.y(0)
    print(circuit)
    amps = run_amplitudes(circuit)
    for idx, amp in enumerate(amps):
        print(f"  |{idx}> amplitude: {amp}")
    print()


def demo_pauli_z() -> None:
    """Pauli-Z on |+> flips the phase: |+> -> |->."""
    print("=== Pauli-Z on |+> ===")
    print("Z|+> = |->")
    circuit = Circuit()
    circuit.h(0)
    circuit.z(0)
    print(circuit)
    amps = run_amplitudes(circuit)
    for idx, amp in enumerate(amps):
        print(f"  |{idx}> amplitude: {amp}")
    probs = run_statevector(circuit)
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print()


def demo_hadamard() -> None:
    """Hadamard on |0> and |1>."""
    print("=== Hadamard on |0> ===")
    h0 = Circuit()
    h0.h(0)
    amps = run_amplitudes(h0)
    for idx, amp in enumerate(amps):
        print(f"  |{idx}> amplitude: {amp}")

    print("\n=== Hadamard on |1> ===")
    h1 = Circuit()
    h1.x(0)
    h1.h(0)
    amps = run_amplitudes(h1)
    for idx, amp in enumerate(amps):
        print(f"  |{idx}> amplitude: {amp}")
    print()


def demo_s_gate() -> None:
    """S gate (phase gate, pi/2 rotation)."""
    print("=== S|+> = (|0> + i|1>)/sqrt(2) ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.s(0)
    print(circuit)
    amps = run_amplitudes(circuit)
    for idx, amp in enumerate(amps):
        print(f"  |{idx}> amplitude: {amp}")
    print()


def demo_t_gate() -> None:
    """T gate (pi/4 rotation)."""
    print("=== T|+> = (|0> + e^(i*pi/4)|1>)/sqrt(2) ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.t(0)
    print(circuit)
    amps = run_amplitudes(circuit)
    for idx, amp in enumerate(amps):
        print(f"  |{idx}> amplitude: {amp}")
    print()


def demo_cx_truth_table() -> None:
    """CNOT truth table (control=qubit 1, target=qubit 0)."""
    print("=== CX truth table (control=q1, target=q0) ===")
    print(f"  {'input':>8}  ->  {'output':>8}")
    print(f"  {'--------':>8}     {'--------':>8}")

    for control, target in ((0, 0), (0, 1), (1, 0), (1, 1)):
        circuit = Circuit()
        if target:
            circuit.x(0)
        if control:
            circuit.x(1)
        circuit.cnot(1, 0)  # control=q1, target=q0
        amps = run_amplitudes(circuit)
        # find which basis state has nonzero amplitude
        out_idx = next(i for i, a in enumerate(amps) if abs(a) > 1e-10)
        out_bits = format(out_idx, "02b")
        print(f"  |{control}{target}>  ->  |{out_bits}>")
    print()


def main() -> None:
    demo_pauli_x()
    demo_pauli_y()
    demo_pauli_z()
    demo_hadamard()
    demo_s_gate()
    demo_t_gate()
    demo_cx_truth_table()


if __name__ == "__main__":
    main()
