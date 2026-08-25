#!/usr/bin/env python3
"""Oracle basics: marking a target state with a phase flip.

A phase oracle flips the sign of the target computational basis state
while leaving all others unchanged.  Here we mark |11> with a CZ gate
and verify the phase flip by inspecting amplitudes.
"""

from __future__ import annotations

import json

from braket.circuits import Circuit, ResultType
from braket.devices import LocalSimulator


def sv_probs(circuit: Circuit) -> tuple[list[complex], dict[str, float]]:
    """Run circuit with statevector + probability result types."""
    circuit.add_result_type(ResultType.StateVector())
    circuit.add_result_type(ResultType.Probability())
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    sv = [complex(a) for a in result.result_types[0].value]
    probs_arr = result.result_types[1].value
    n_qubits = len(sv).bit_length() - 1
    probs = {format(i, f"0{n_qubits}b"): round(float(p), 6)
             for i, p in enumerate(probs_arr)}
    return sv, probs


def oracle_mark_11() -> Circuit:
    """Build a 2-qubit oracle that marks |11> with a phase flip.

    CZ(q0, q1) applies a -1 phase exactly when both qubits are |1>.
    """
    circuit = Circuit()
    circuit.cz(0, 1)
    return circuit


def demo_mark_11_from_zero() -> None:
    """Apply the oracle to |00> — nothing happens (|11> has zero amplitude)."""
    print("=== Oracle on |00> ===")
    circuit = oracle_mark_11()
    sv, probs = sv_probs(circuit)
    print(f"amplitudes: {sv}")
    print(f"probabilities: {json.dumps(probs)}")
    print("No phase flip — |11> is not present in the state.")
    print()


def demo_mark_11_in_superposition() -> None:
    """Put both qubits in superposition, then apply the oracle.

    H(0) H(1) creates (|00> + |01> + |10> + |11>)/2.
    The oracle flips only the |11> component.
    """
    print("=== Oracle on equal superposition ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.h(1)
    circuit.cz(0, 1)

    sv, probs = sv_probs(circuit)
    print(f"amplitudes: {sv}")
    print(f"probabilities: {json.dumps(probs)}")
    print("Only |11> has its sign flipped — the others are unchanged.")
    print()


def demo_two_oracles() -> None:
    """Compare marking |10> vs |01>."""
    targets = {
        "|10>": 2,
        "|01>": 1,
    }

    for label, target in targets.items():
        print(f"=== Oracle marking {label} ===")
        circuit = Circuit()
        circuit.h(0)
        circuit.h(1)

        bits = format(target, "02b")
        if bits[1] == "0":
            circuit.x(0)
        if bits[0] == "0":
            circuit.x(1)
        circuit.cz(0, 1)
        if bits[1] == "0":
            circuit.x(0)
        if bits[0] == "0":
            circuit.x(1)

        sv, probs = sv_probs(circuit)
        print(f"amplitudes: {sv}")
        print(f"probabilities: {json.dumps(probs)}")
        print()


def main() -> None:
    demo_mark_11_from_zero()
    demo_mark_11_in_superposition()
    demo_two_oracles()


if __name__ == "__main__":
    main()
