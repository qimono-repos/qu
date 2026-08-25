#!/usr/bin/env python3
"""Controlled gates: CNOT, CZ.

Show the truth table for each two-qubit controlled gate by preparing
all four computational-basis inputs and inspecting the output.
"""

from __future__ import annotations

import json

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def run_amplitudes(circuit: Circuit) -> list[complex]:
    """Return the statevector (amplitudes) for a circuit."""
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    return result.result_types[0].value


def demo_cnot() -> None:
    """CNOT (C-X): flips target when control is |1>."""
    print("=== CNOT (CX) truth table ===")
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
        out_idx = next(i for i, a in enumerate(amps) if abs(a) > 1e-10)
        out_bits = format(out_idx, "02b")
        print(f"  |{control}{target}>  ->  |{out_bits}>")
    print()
    print("CX flips qubit 0 when qubit 1 is |1>.")
    print("In Braket bitstrings: qubit 1 is the left bit, qubit 0 is the right bit.")
    print()


def demo_cz() -> None:
    """CZ: flips sign of |11> component."""
    print("=== CZ truth table ===")
    print("  CZ is diagonal: it only adds a phase to |11>.")
    print("  |00> -> |00>,  |01> -> |01>,  |10> -> |10>,  |11> -> -|11>")
    print()

    device = LocalSimulator()
    for i in range(4):
        bits = format(i, "02b")
        circuit = Circuit()
        if bits[1] == "1":
            circuit.x(1)
        if bits[0] == "1":
            circuit.x(0)
        circuit.cz(1, 0)  # control=q1, target=q0
        result = device.run(circuit, shots=0).result()
        amps = result.result_types[0].value
        for idx, amp in enumerate(amps):
            if abs(amp) > 1e-10:
                basis = format(idx, "02b")
                print(f"  |{bits}> -> {amp:.4f} |{basis}>")
    print()


def demo_cnot_shots() -> None:
    """CNOT with superposition input and measurement statistics."""
    print("=== CNOT with H on control ===")
    circuit = Circuit()
    circuit.h(1)       # put control in superposition
    circuit.cnot(1, 0) # CNOT
    circuit.measure(0)
    circuit.measure(1)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=2000).result()
    counts = result.result_types[0].value
    print(f"counts: {counts}")
    print("Expect |00> and |11> ~50/50 — the Bell state Phi+.")
    print()


def main() -> None:
    demo_cnot()
    demo_cz()
    demo_cnot_shots()


if __name__ == "__main__":
    main()
