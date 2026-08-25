#!/usr/bin/env python3
"""Phase kickback: the eigenvalue of a unitary kicks back as a phase
onto the control qubit.

Phase kickback is the engine behind Grover's diffuser, QPE, and the
Deutsch–Jozsa ancilla. When a control qubit in |+> targets an
eigenvector |u> of U with eigenvalue e^{i phi}, the controlled-U
maps:

    |+>|u>  ->  (cos(phi/2)|0> + sin(phi/2)|1>) |u>

This demo uses the oracle from the oracle-basics example (Toffoli
marking |11>) with the ancilla in |->. We show the statevector,
the Bloch vector, and explain why single-qubit measurement gives 50/50.
"""

from __future__ import annotations

import math

import qiskit as qk
import qiskit_aer as qka


def toffoli_oracle() -> qk.QuantumCircuit:
    """Bit-flip oracle: Toffoli on q0, q1, q2. Marks |11> on inputs."""
    qc = qk.QuantumCircuit(3, name="Toffoli")
    qc.ccx(0, 1, 2)
    return qc


def phase_kickback_circuit() -> qk.QuantumCircuit:
    """|+>|+>|-> with Toffoli oracle.

    q0, q1 = input qubits in |+>
    q2 = ancilla in |-> (the -1 eigenstate of the oracle)
    """
    qc = qk.QuantumCircuit(3)
    qc.h(0)
    qc.h(1)
    qc.x(2)
    qc.h(2)
    qc.compose(toffoli_oracle(), inplace=True)
    return qc


def statevector_analysis() -> None:
    """Show the full 3-qubit statevector and reduced states."""
    qc = phase_kickback_circuit()
    sv = qk.quantum_info.Statevector.from_instruction(qc)

    print("  3-qubit statevector after oracle:")
    print("  state        amp                      prob")
    print("  " + "-" * 52)
    probs = sv.probabilities_dict()
    for state in sorted(probs.keys()):
        amp = sv.data[int(state[::-1], 2)]
        p = probs[state]
        if p > 1e-6:
            sign = "+" if amp.real >= 0 else "-"
            print(f"  |{state}>  {sign}{abs(amp):.6f}            {p:.4f}")

    # Reduced state of input qubits (q0, q1)
    rho_in = qk.quantum_info.partial_trace(sv, [2])
    rd = rho_in.data
    print(f"\n  Input qubits (q0,q1) reduced density matrix:")
    print(f"    diagonal: [{rd[0,0].real:.4f}, {rd[1,1].real:.4f}, "
          f"{rd[2,2].real:.4f}, {rd[3,3].real:.4f}]")
    print(f"    (maximally mixed: each basis state has equal probability)")

    # show the phase pattern
    print(f"\n  Phase pattern on the input register:")
    print(f"    |00> -> +  (f(00)=0, no phase)")
    print(f"    |01> -> +  (f(01)=0, no phase)")
    print(f"    |10> -> +  (f(10)=0, no phase)")
    print(f"    |11> -> -  (f(11)=1, phase kickback!)")
    print(f"\n  The phase (-1)^{{f(x)}} is in the two-qubit amplitudes.")
    print(f"  Tracing out the ancilla gives I/4 (maximally mixed),")
    print(f"  so no single-qubit measurement reveals the phase.")
    print()


def measurement_demo() -> None:
    """Show that single-qubit measurements give 50/50."""
    print("--- single-qubit measurement ---\n")
    qc = qk.QuantumCircuit(3, 3)
    qc.h(0)
    qc.h(1)
    qc.x(2)
    qc.h(2)
    qc.compose(toffoli_oracle(), inplace=True)
    qc.measure([0, 1, 2], [0, 1, 2])
    print(qc.draw(output="text"))

    backend = qka.AerSimulator()
    counts = backend.run(qk.transpile(qc, backend), shots=4096).result().get_counts()
    print("\nshot histogram:")
    for bits, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  |{bits}>  {n:4d}")

    print(f"\n  All 8 outcomes are equally likely (~500 each).")
    print(f"  The phase kickback (-1 on |11>) is invisible here!")
    print()


def grover_contrast() -> None:
    """Show that adding the Grover diffusion step MAKES the phase visible."""
    print("--- Grover: oracle + diffusion makes the phase visible ---\n")
    n = 2
    qc = qk.QuantumCircuit(n + 1, n)
    # prepare |+>^n on inputs, |-> on ancilla
    qc.h(0)
    qc.h(1)
    qc.x(2)
    qc.h(2)
    # oracle: Toffoli marks |11>
    qc.ccx(0, 1, 2)
    # diffusion on input qubits: 2|s><s| - I
    qc.h(0)
    qc.h(1)
    qc.x(0)
    qc.x(1)
    qc.h(1)
    qc.cx(0, 1)
    qc.h(1)
    qc.x(0)
    qc.x(1)
    qc.h(0)
    qc.h(1)
    qc.measure([0, 1], [0, 1])
    print(qc.draw(output="text"))

    backend = qka.AerSimulator()
    counts = backend.run(qk.transpile(qc, backend), shots=4096).result().get_counts()
    print("\nshot histogram:")
    for bits, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        flag = "  <-- marked" if bits == "11" else ""
        print(f"  |{bits}>  {n:4d}{flag}")

    print(f"\n  After one Grover iterate, |11> is amplified!")
    print(f"  The diffusion step converts the phase (invisible) into")
    print(f"  an amplitude (visible in measurement).")
    print()


def main() -> None:
    print("=== Phase kickback ===\n")
    statevector_analysis()
    measurement_demo()
    grover_contrast()
    print("=== done ===")


if __name__ == "__main__":
    main()
