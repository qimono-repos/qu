#!/usr/bin/env python3
"""Phase kickback demonstration.

Phase kickback occurs when a controlled oracle acts on an eigenstate of
the oracle: the eigenvalue phase is "kicked back" onto the control
qubit.  This is the core mechanism behind Deutsch-Jozsa, Grover, and
phase estimation.

We demonstrate with a 1-bit Deutsch oracle (balanced function f(x)=x)
where the ancilla is prepared in |-> so that the oracle's phase is
transferred to the input qubit.
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


def demo_basic_kickback() -> None:
    """Show phase kickback with a CNOT-based oracle.

    Oracle: CNOT(q0, q1) computes f(x) = x into the ancilla.
    Ancilla starts in |-> = (|0> - |1>)/sqrt(2).

    When input is |0>:  |0>|-> --CNOT-->  |0>|->   (no change)
    When input is |1>:  |1>|-> --CNOT-->  -|1>|->  (phase kickback to q0)
    """
    print("=== Phase kickback with balanced oracle f(x) = x ===")

    for inp in (0, 1):
        circuit = Circuit()
        if inp:
            circuit.x(0)
        circuit.h(0)
        circuit.x(1)
        circuit.h(1)
        circuit.cnot(0, 1)

        sv, probs = sv_probs(circuit)
        print(f"input |{inp}>: amplitudes = {sv}")
        print(f"         probabilities = {json.dumps(probs)}")
        if inp == 0:
            print("  |0>|-> unchanged — no phase kickback.")
        else:
            print("  -|1>|-> — phase -1 kicked back onto q0.")
        print()


def demo_superposition_kickback() -> None:
    """Input in superposition: kickback produces entanglement.

    H(0) creates (|0>+|1>)/sqrt(2) as input.
    Oracle CNOT(0,1) on |-> ancilla gives:
      (|0>|-> + |1>(-|->))/sqrt(2) = (|0> - |1>)/sqrt(2) |-> = H(0)|->|->

    After uncomputing H(0), the input qubit collapses to |1>.
    """
    print("=== Kickback from superposition input ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.x(1)
    circuit.h(1)
    circuit.cnot(0, 1)
    circuit.h(0)

    sv, probs = sv_probs(circuit)
    print(f"amplitudes: {sv}")
    print(f"probabilities: {json.dumps(probs)}")
    print("After H-uncompute, qubit 0 is |1> — the balanced function's")
    print("output was kicked back and revealed by the final Hadamard.")
    print()


def demo_phase_oracle_kickback() -> None:
    """Phase oracle on |+> ancilla: cleanest kickback demo.

    Oracle Z on q0 (phase flip on |1>), ancilla q1 in |->:
      |0>|-> --Z(0)-->  |0>|->    (no effect on |0>)
      |1>|-> --Z(0)--> -|1>|->    (phase -1 on |1>)

    With q0 in |+>, the oracle produces (|0> - |1>)/sqrt(2) = Z|+>.
    """
    print("=== Phase oracle kickback with |+> input ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.x(1)
    circuit.h(1)
    circuit.cz(0, 1)

    sv, probs = sv_probs(circuit)
    print(f"amplitudes: {sv}")
    print(f"probabilities: {json.dumps(probs)}")
    print("The CZ phase oracle applied to |+>|-> gives |->|->.")
    print("The phase was kicked back from the ancilla to the input.")
    print()


def main() -> None:
    demo_basic_kickback()
    demo_superposition_kickback()
    demo_phase_oracle_kickback()


if __name__ == "__main__":
    main()
