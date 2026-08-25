#!/usr/bin/env python3
"""Quantum Phase Estimation (QPE) on a simple unitary.

QPE estimates the phase phi in the eigenvalue equation U|psi> = e^{2*pi*i*phi}|psi>.
With n precision qubits, it determines phi to n bits of accuracy.

We use U = Z (Pauli-Z) on |1>, which has eigenvalue -1 = e^{i*pi},
so phi = 1/2 = 0.1 in binary.
"""

from __future__ import annotations

import cmath

from braket.circuits import Circuit
from braket.devices import LocalSimulator


def _add_inverse_qft(circuit: Circuit, n: int) -> None:
    """Add inverse QFT to the precision register (qubits 0..n-1)."""
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            k = j - i + 1
            angle = -2.0 * cmath.pi / (2**k)
            circuit.cphaseshift(j, i, angle)
        circuit.h(i)


def qpe_circuit(precision_bits: int = 2) -> Circuit:
    """Build the QPE circuit.

    Qubits 0..precision_bits-1: precision register (starts in |0>).
    Qubit precision_bits: target (eigenstate |1>).

    Steps:
      1. X on target to prepare |1> eigenstate of Z.
      2. H on all precision qubits.
      3. Controlled-U^{2^k} for each precision qubit k.
      4. Inverse QFT on precision register.
      5. Measure precision qubits.
    """
    circuit = Circuit()
    n = precision_bits
    target = n

    circuit.x(target)
    for i in range(n):
        circuit.h(i)

    for k in range(n):
        power = 2**k
        circuit.cphaseshift(k, target, power * cmath.pi)

    _add_inverse_qft(circuit, n)

    for i in range(n):
        circuit.measure(i)
    return circuit


def demo_qpe_2bits() -> None:
    """QPE with 2 precision bits on Z|1> (phi = 1/2 = 0.1 binary)."""
    print("=== QPE: U = Z, |psi> = |1>, phi = 1/2 ===")
    circuit = qpe_circuit(precision_bits=2)
    print(circuit)

    device = LocalSimulator()
    result = device.run(circuit, shots=1000).result()
    counts = dict(result.measurement_counts)

    print(f"counts: {counts}")
    for bits, n_shots in sorted(counts.items()):
        measured_phi = int(bits, 2) / 4
        print(f"  |{bits}> -> phi = {measured_phi:.2f}")
    print("Expected: phi = 0.50")
    print()


def demo_qpe_3bits() -> None:
    """QPE with 3 precision bits on Z|1> (phi = 1/2 = 0.100 binary)."""
    print("=== QPE: U = Z, |psi> = |1>, 3 precision bits ===")
    circuit = qpe_circuit(precision_bits=3)

    device = LocalSimulator()
    result = device.run(circuit, shots=1000).result()
    counts = dict(result.measurement_counts)

    print(f"counts: {counts}")
    for bits, n_shots in sorted(counts.items()):
        measured_phi = int(bits, 2) / 8
        print(f"  |{bits}> -> phi = {measured_phi:.3f}")
    print("Expected: phi = 0.500")
    print()


def demo_qpe_phase_gate() -> None:
    """QPE on the phase gate R(theta) with theta = pi/3."""
    print("=== QPE: U = PhaseGate(pi/3), 3 precision bits ===")
    print("eigenvalue = e^{i*pi/3}, so phi = 1/6 ~ 0.1667")
    print()

    n = 3
    target = n
    theta = cmath.pi / 3

    circuit = Circuit()
    circuit.x(target)
    for i in range(n):
        circuit.h(i)

    for k in range(n):
        power = 2**k
        circuit.cphaseshift(k, target, power * theta)

    _add_inverse_qft(circuit, n)
    for i in range(n):
        circuit.measure(i)

    device = LocalSimulator()
    result = device.run(circuit, shots=1000).result()
    counts = dict(result.measurement_counts)

    print(f"counts: {counts}")
    for bits, n_shots in sorted(counts.items()):
        measured_phi = int(bits, 2) / 8
        print(f"  |{bits}> -> phi = {measured_phi:.4f}")
    print("Expected: phi = 0.1667")


def main() -> None:
    demo_qpe_2bits()
    demo_qpe_3bits()
    demo_qpe_phase_gate()


if __name__ == "__main__":
    main()
