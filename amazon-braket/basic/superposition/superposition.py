#!/usr/bin/env python3
"""Superposition with Hadamard, then entanglement with CNOT.

This file is a self-contained Bell-pair walkthrough. It does not import
any helpers from the other example folders.
"""

from __future__ import annotations

import json

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def single_qubit_superposition() -> Circuit:
    """Put one qubit on the equator of the Bloch sphere: H|0> = |+>."""
    circuit = Circuit()
    circuit.h(0)
    circuit.measure(0)
    return circuit


def bell_phi_plus() -> Circuit:
    """Build |Phi+> = (|00> + |11>)/sqrt(2) with H then CNOT."""
    circuit = Circuit()
    circuit.h(0)
    circuit.cnot(0, 1)
    return circuit


def bell_psi_minus() -> Circuit:
    """A different Bell state, built from scratch: (|01> - |10>)/sqrt(2)."""
    circuit = Circuit()
    circuit.x(1)
    circuit.h(0)
    circuit.z(0)
    circuit.cnot(0, 1)
    return circuit


def sample_bell(circuit: Circuit) -> dict[str, int]:
    """Measure a Bell state with shots and return counts."""
    measured = Circuit()
    measured.add_circuit(circuit)
    measured.measure(0)
    measured.measure(1)
    device = LocalSimulator()
    result = device.run(measured, shots=4096).result()
    return result.result_types[0].value


def correlation(counts: dict[str, int]) -> float:
    """P(bits equal) - P(bits different) for a two-qubit shot histogram."""
    agree = disagree = 0
    for bitstring, n in counts.items():
        bits = bitstring.replace(" ", "")
        if bits[0] == bits[1]:
            agree += n
        else:
            disagree += n
    total = agree + disagree
    return (agree - disagree) / total


def main() -> None:
    device = LocalSimulator()

    # Single-qubit superposition
    plus = single_qubit_superposition()
    print("=== single-qubit superposition (Hadamard) ===")
    print(plus)
    result = device.run(plus, shots=4096).result()
    counts = result.result_types[0].value
    print(f"shots=4096: {counts}")
    print("expect roughly half |0> and half |1>")
    print()

    # Bell Phi+
    phi = bell_phi_plus()
    print("=== Bell |Phi+> via H then CNOT ===")
    print(phi)
    sv_result = device.run(phi, shots=0).result()
    amps = sv_result.result_types[0].value
    probs = sv_result.result_types[1].value
    print(f"amplitudes: {amps}")
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")

    phi_counts = sample_bell(phi)
    print(f"|Phi+> shots=4096: {phi_counts}")
    print(f"|Phi+> ZZ correlation: {correlation(phi_counts):+.3f}")
    print("only |00> and |11> should appear — the qubits are entangled")
    print()

    # Bell Psi-
    psi = bell_psi_minus()
    print("=== Bell |Psi-> (independent circuit) ===")
    print(psi)
    sv_result = device.run(psi, shots=0).result()
    amps = sv_result.result_types[0].value
    probs = sv_result.result_types[1].value
    print(f"amplitudes: {amps}")
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")

    psi_counts = sample_bell(psi)
    print(f"|Psi-> shots=4096: {psi_counts}")
    print(f"|Psi-> ZZ correlation: {correlation(psi_counts):+.3f}")


if __name__ == "__main__":
    main()
