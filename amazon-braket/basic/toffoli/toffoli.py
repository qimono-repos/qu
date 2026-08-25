#!/usr/bin/env python3
"""Toffoli (CCX) gate: a reversible AND, written as its own circuit.

The Toffoli flips the target only when both controls are |1>. With the
target starting at |0> that is exactly the classical AND of the controls,
stored reversibly. This file does not share code with the other examples.
"""

from __future__ import annotations

import json

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def toffoli_on(controls: tuple[int, int], target: int) -> Circuit:
    """Prepare |c1 c0 t> and apply CCX(c1, c0, t).

    Qubit 2 is the high control, qubit 1 the low control, qubit 0 the
    target, matching Braket's bitstring convention (|q2 q1 q0>).
    """
    c1, c0 = controls
    circuit = Circuit()
    if target:
        circuit.x(0)
    if c0:
        circuit.x(1)
    if c1:
        circuit.x(2)
    circuit.ccnot(2, 1, 0)
    return circuit


def truth_table() -> None:
    """Print the full truth table for Toffoli."""
    print("=== Toffoli truth table  (c1 c0 t  ->  c1 c0 t') ===")
    print("c1 c0 t | c1 c0 t'")
    print("--------+---------")
    device = LocalSimulator()
    for c1 in (0, 1):
        for c0 in (0, 1):
            for t in (0, 1):
                circuit = toffoli_on((c1, c0), t)
                result = device.run(circuit, shots=0).result()
                amps = result.result_types[0].value
                out_idx = next(i for i, a in enumerate(amps) if abs(a) > 1e-10)
                out_bits = format(out_idx, "03b")
                print(f" {c1}  {c0}  {t} |  {out_bits[0]}  {out_bits[1]}  {out_bits[2]}")


def reversible_and() -> None:
    """Show that Toffoli computes AND when target starts at |0>."""
    print("\n=== reversible AND: |c1 c0 0> --CCX--> |c1 c0 (c1 AND c0)> ===")
    device = LocalSimulator()
    for c1, c0 in ((0, 0), (0, 1), (1, 0), (1, 1)):
        circuit = toffoli_on((c1, c0), 0)
        result = device.run(circuit, shots=0).result()
        amps = result.result_types[0].value
        out_idx = next(i for i, a in enumerate(amps) if abs(a) > 1e-10)
        out_bits = format(out_idx, "03b")
        print(f"  {c1} AND {c0} = {out_bits[2]}   (full ket |{out_bits}>)")


def superposition_controls() -> None:
    """Both controls in superposition: the target becomes a GHZ-like AND."""
    circuit = Circuit()
    circuit.h(1)
    circuit.h(2)
    circuit.ccnot(2, 1, 0)
    circuit.measure(0)
    circuit.measure(1)
    circuit.measure(2)

    print("\n=== CCX with controls in equal superposition ===")
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=2048).result()
    counts = result.result_types[0].value
    print("counts (bitstring = q2 q1 q0):")
    for bits, n in sorted(counts.items()):
        print(f"  |{bits}>  {n}")
    print("the target bit is 1 only in |111> — that is the AND of the controls")


def main() -> None:
    circuit = Circuit()
    circuit.ccnot(2, 1, 0)
    print("Toffoli circuit (controls q2,q1  target q0)")
    print(circuit)
    print()
    truth_table()
    reversible_and()
    superposition_controls()


if __name__ == "__main__":
    main()
