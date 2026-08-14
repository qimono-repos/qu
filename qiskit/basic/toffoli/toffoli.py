#!/usr/bin/env python3
"""Toffoli (CCX) gate: a reversible AND, written as its own circuit.

The Toffoli flips the target only when both controls are |1>. With the
target starting at |0> that is exactly the classical AND of the controls,
stored reversibly. This file does not share code with the other examples.
"""

from __future__ import annotations

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


def toffoli_on(controls: tuple[int, int], target: int) -> QuantumCircuit:
    """Prepare |c1 c0 t> and apply CCX(c1, c0, t).

    Qubit 2 is the high control, qubit 1 the low control, qubit 0 the
    target, matching Qiskit's little-endian drawing (|q2 q1 q0>).
    """
    c1, c0 = controls
    qc = QuantumCircuit(3, name="toffoli")
    if target:
        qc.x(0)
    if c0:
        qc.x(1)
    if c1:
        qc.x(2)
    qc.ccx(2, 1, 0)
    return qc


def truth_table() -> None:
    print("=== Toffoli truth table  (c1 c0 t  ->  c1 c0 t') ===")
    print("c1 c0 t | c1 c0 t'")
    print("--------+---------")
    for c1 in (0, 1):
        for c0 in (0, 1):
            for t in (0, 1):
                qc = toffoli_on((c1, c0), t)
                bits = next(iter(Statevector.from_instruction(qc).to_dict()))
                print(f" {c1}  {c0}  {t} |  {bits[0]}  {bits[1]}  {bits[2]}")


def reversible_and() -> None:
    print("\n=== reversible AND: |c1 c0 0> --CCX--> |c1 c0 (c1 AND c0)> ===")
    for c1, c0 in ((0, 0), (0, 1), (1, 0), (1, 1)):
        qc = toffoli_on((c1, c0), 0)
        bits = next(iter(Statevector.from_instruction(qc).to_dict()))
        print(f"  {c1} AND {c0} = {bits[2]}   (full ket |{bits}>)")


def superposition_controls() -> None:
    """Both controls in superposition: the target becomes a GHZ-like AND."""
    qc = QuantumCircuit(3, 3, name="toffoli_superposed")
    qc.h(1)
    qc.h(2)
    qc.ccx(2, 1, 0)
    qc.measure([0, 1, 2], [0, 1, 2])

    print("\n=== CCX with controls in equal superposition ===")
    print(qc.draw(output="text"))
    backend = AerSimulator()
    counts = backend.run(transpile(qc, backend), shots=2048).result().get_counts()
    print("counts (bitstring = q2 q1 q0):")
    for bits, n in sorted(counts.items()):
        print(f"  |{bits}>  {n}")
    print("the target bit is 1 only in |111> — that is the AND of the controls")


def main() -> None:
    demo = QuantumCircuit(3, name="toffoli")
    demo.ccx(2, 1, 0)
    print("Toffoli circuit (controls q2,q1  target q0)")
    print(demo.draw(output="text"))
    print()
    truth_table()
    reversible_and()
    superposition_controls()


if __name__ == "__main__":
    main()
