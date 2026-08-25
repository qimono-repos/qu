"""Superposition: Hadamard on |0⟩ with 50/50 measurement statistics."""

import cirq


def main() -> None:
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(q), cirq.measure(q, key="m"))

    print("=== Hadamard creates superposition ===")
    print(circuit)

    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1000)
    counts = result.histogram(key="m")

    print(f"\nMeasurement results (1000 shots):")
    for k in sorted(counts):
        print(f"  |{k}⟩: {counts[k]} ({counts[k]/10:.1f}%)")

    total = sum(counts.values())
    ratio = counts[0] / total if 0 in counts else 0
    print(f"\nRatio |0⟩/total: {ratio:.3f} (ideal: 0.500)")

    print("\n=== State vector before measurement ===")
    circuit_no_meas = cirq.Circuit(cirq.H(q))
    result = sim.simulate(circuit_no_meas)
    sv = result.final_state_vector
    print(f"|ψ⟩ = {sv[0]:.4f}|0⟩ + {sv[1]:.4f}|1⟩")
    print(f"P(|0⟩) = {abs(sv[0])**2:.4f},  P(|1⟩) = {abs(sv[1])**2:.4f}")

    print("\n=== Bell pair superposition (2 qubits) ===")
    q0, q1 = cirq.LineQubit.range(2)
    bell = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key="m"))
    print(bell)
    result = sim.run(bell, repetitions=1000)
    counts = result.histogram(key="m")
    for k in sorted(counts):
        print(f"  |{k:02b}⟩: {counts[k]} ({counts[k]/10:.1f}%)")


if __name__ == "__main__":
    main()
