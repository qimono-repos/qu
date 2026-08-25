#!/usr/bin/env python3
"""Oracle basics: build a simple oracle that marks |11> and show the
input/output relationship.

An oracle is a unitary O_f that maps |x>|y> to |x>|y XOR f(x)>.
A phase oracle instead maps |x> to (-1)^{f(x)} |x>. This demo
builds both forms for f(x) = x_0 AND x_1 (marks only |11>) on
two qubits and verifies the action with statevector simulation.
"""

from __future__ import annotations

import qiskit as qk
import qiskit_aer as qka


def bitflip_oracle() -> qk.QuantumCircuit:
    """Bit-flip oracle: |x>|y> -> |x>|y XOR (x0 AND x1)>.

    Two input qubits (q0, q1) and one target qubit (q2).
    A Toffoli flips q2 exactly when both inputs are |1>.
    """
    qc = qk.QuantumCircuit(3, name="bitflip oracle")
    qc.ccx(0, 1, 2)
    return qc


def phase_oracle() -> qk.QuantumCircuit:
    """Phase oracle: |x> -> (-1)^{x0 AND x1} |x>.

    Equivalent to a controlled-Z gate on the two input qubits.
    """
    qc = qk.QuantumCircuit(2, name="phase oracle")
    qc.cz(0, 1)
    return qc


def bitflip_oracle_with_ancilla() -> qk.QuantumCircuit:
    """Bit-flip oracle with ancilla initially in |->.

    The ancilla in |-> picks up a phase kickback:
    |x>|-> -> (-1)^{f(x)} |x>|->.
    """
    qc = qk.QuantumCircuit(3, name="bitflip+kickback")
    qc.x(2)
    qc.h(2)
    qc.ccx(0, 1, 2)
    return qc


def main() -> None:
    print("=== Oracle basics ===\n")

    # --- bit-flip oracle demo ---
    print("1) Bit-flip oracle: |x0 x1 y> -> |x0 x1 y XOR (x0 AND x1)>")
    print("   initial state: |0>|0>|0>\n")
    qc = qk.QuantumCircuit(3, 3)
    # prepare inputs in superposition to see all cases at once
    qc.h(0)
    qc.h(1)
    # ancilla stays |0>
    qc.compose(bitflip_oracle(), inplace=True)
    qc.measure(range(3), range(3))
    print(qc.draw(output="text"))

    backend = qka.AerSimulator()
    counts = backend.run(qk.transpile(qc, backend), shots=4096).result().get_counts()
    print("shot results (q0 q1 y, little-endian):")
    for bits, n in sorted(counts.items()):
        print(f"  |{bits}>  {n:4d}")

    print("\n  reading: when inputs are |11> the target flips to |1>.\n")

    # --- phase oracle demo ---
    print("2) Phase oracle: |x> -> (-1)^{x0 AND x1} |x>")
    print("   prepare |+>|+> = (|00>+|01>+|10>+|11>)/2\n")
    qc2 = qk.QuantumCircuit(2)
    qc2.h(0)
    qc2.h(1)
    qc2.compose(phase_oracle(), inplace=True)
    sv = qk.quantum_info.Statevector.from_instruction(qc2)
    probs = sv.probabilities_dict()
    phases = sv.data
    for state in ["00", "01", "10", "11"]:
        amp = phases[int(state[::-1], 2)]
        sign = "+" if amp.real >= 0 else "-"
        print(f"  |{state}>  amp = {sign}{abs(amp):.4f}  p = {probs[state]:.4f}")

    print("\n  only |11> picks up the -1 phase; probabilities stay uniform.\n")

    # --- kickback demo ---
    print("3) Bit-flip oracle + ancilla |-> -> phase kickback")
    print("   ancilla stays |-> after the oracle; phase is in the amplitudes.\n")
    qc3 = qk.QuantumCircuit(3)
    qc3.h(0)
    qc3.h(1)
    qc3.compose(bitflip_oracle_with_ancilla(), inplace=True)
    sv3 = qk.quantum_info.Statevector.from_instruction(qc3)
    probs3 = sv3.probabilities_dict()
    for state in sorted(probs3.keys()):
        amp = sv3.data[int(state[::-1], 2)]
        p = probs3[state]
        sign = "+" if amp.real >= 0 else "-"
        print(f"  |{state}>  {sign}{abs(amp):.4f}  p = {p:.4f}")

    print("\n  the phase (-1)^{f(x)} is in the two-qubit amplitudes.")
    print("  the input qubits are maximally mixed (50/50 each).")
    print("  the phase kickback is invisible in single-qubit measurement!\n")

    print("=== done ===")


if __name__ == "__main__":
    main()
