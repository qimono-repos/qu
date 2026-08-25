#!/usr/bin/env python3
"""Quantum teleportation protocol.

Alice has a qubit in an unknown state |psi>. She and Bob share a Bell
pair. After a Bell measurement and classical communication, Bob applies
corrections to recover |psi> on his qubit.
"""

from __future__ import annotations

import qiskit as qk
import qiskit_aer as qka


def teleport_circuit(theta: float = 0.7, phi: float = 1.2) -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(3, 3, name="teleport")

    qc.ry(theta, 0)
    qc.rz(phi, 0)

    qc.h(1)
    qc.cx(1, 2)

    qc.cx(0, 1)
    qc.h(0)

    qc.measure(0, 0)
    qc.measure(1, 1)

    qc.x(2).c_if(1, 1)
    qc.z(2).c_if(0, 1)

    qc.measure(2, 2)

    return qc


def verify_teleportation(theta: float, phi: float, counts: dict[str, int]) -> None:
    expected_0 = (1 + qk.quantum_info.Statevector.from_instruction(
        qk.QuantumCircuit(1)
    ).data[0].real) / 2

    psi = qk.quantum_info.Statevector.from_instruction(
        _prepare_state(theta, phi)
    )
    probs = psi.probabilities_dict()
    print(f"  Original state probabilities: {probs}")

    teleported = qk.quantum_info.Statevector.from_instruction(
        _prepare_state(theta, phi)
    )
    teleported_probs = teleported.probabilities_dict()
    print(f"  Teleported state probabilities: {teleported_probs}")

    total = sum(counts.values())
    measured_0 = sum(v for k, v in counts.items() if k[0] == '0')
    measured_1 = sum(v for k, v in counts.items() if k[0] == '1')
    print(f"  Measurement on target qubit: |0>={measured_0}/{total}, |1>={measured_1}/{total}")
    print(f"  Expected: |0> ~ {teleported_probs.get('0', 0):.4f}, |1> ~ {teleported_probs.get('1', 0):.4f}")


def _prepare_state(theta: float, phi: float) -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(1)
    qc.ry(theta, 0)
    qc.rz(phi, 0)
    return qc


def main() -> None:
    print("=== Quantum Teleportation ===\n")

    theta, phi = 0.7, 1.2
    psi = qk.quantum_info.Statevector.from_instruction(_prepare_state(theta, phi))
    print(f"State to teleport (theta={theta}, phi={phi}):")
    print(f"  {psi}\n")

    qc = teleport_circuit(theta, phi)
    print(qc.draw(output="text"))

    backend = qka.AerSimulator()
    compiled = qk.transpile(qc, backend)
    counts = backend.run(compiled, shots=4096).result().get_counts()

    print(f"\nMeasurement results (c2 c1 c0 = target Alice_Bob Alice_Bob):")
    for bitstring, shots in sorted(counts.items(), key=lambda kv: -kv[1])[:8]:
        print(f"  {bitstring}: {shots}")

    print("\nVerifying teleportation:")
    verify_teleportation(theta, phi, counts)

    print("\n--- Testing multiple states ---\n")
    for name, t, p in [("|0>", 0, 0), ("|1>", 3.14159, 0), ("|+>", 1.5708, 0)]:
        qc = teleport_circuit(t, p)
        compiled = qk.transpile(qc, backend)
        counts = backend.run(compiled, shots=2048).result().get_counts()
        total = sum(counts.values())
        m0 = sum(v for k, v in counts.items() if k[0] == '0')
        m1 = sum(v for k, v in counts.items() if k[0] == '1')
        print(f"  Teleported {name}: |0>={m0}/{total} ({m0/total:.3f}), |1>={m1}/{total} ({m1/total:.3f})")


if __name__ == "__main__":
    main()
