"""Entanglement: Bell state creation and correlation measurements."""

import cirq


def main() -> None:
    q0, q1 = cirq.LineQubit.range(2)
    sim = cirq.Simulator()

    print("=== Bell State Creation ===\n")
    bell = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    print(bell)

    result = sim.simulate(bell)
    sv = result.final_state_vector
    print(f"State: {sv}")
    print("This is (|00⟩ + |11⟩)/√2 — a maximally entangled Bell state.\n")

    print("=== Correlation Measurements ===\n")
    bell_meas = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key="m"))
    result = sim.run(bell_meas, repetitions=1000)
    counts = result.histogram(key="m")
    print(f"  |00⟩: {counts.get(0, 0)},  |01⟩: {counts.get(1, 0)},  |10⟩: {counts.get(2, 0)},  |11⟩: {counts.get(3, 0)}")
    print("  → Only |00⟩ and |11⟩ appear (correlated results).\n")

    print("=== All Four Bell States ===\n")
    bell_states: dict[str, list[cirq.Operation]] = {
        "|Φ+⟩": [cirq.H(q0), cirq.CNOT(q0, q1)],
        "|Φ-⟩": [cirq.X(q0), cirq.H(q0), cirq.CNOT(q0, q1)],
        "|Ψ+⟩": [cirq.H(q0), cirq.CNOT(q0, q1), cirq.X(q1)],
        "|Ψ-⟩": [cirq.X(q0), cirq.H(q0), cirq.CNOT(q0, q1), cirq.X(q1)],
    }

    for label, ops in bell_states.items():
        result = sim.simulate(cirq.Circuit(ops))
        sv = result.final_state_vector
        print(f"  {label}: {sv}")

    print("\n=== Entanglement vs Separable States ===\n")

    print("Separable |+⟩ ⊗ |+⟩:")
    sep = cirq.Circuit(cirq.H(q0), cirq.H(q1))
    sv = sim.simulate(sep).final_state_vector
    print(f"  State: {sv}")
    print(f"  Product: {sv[0]*sv[0]:.4f} = P(|00⟩), etc.\n")

    print("Entangled Bell |Φ+⟩:")
    sv = sim.simulate(bell).final_state_vector
    print(f"  State: {sv}")
    print("  Cannot be factored as a product of single-qubit states.")

    print("\n=== Measuring one qubit collapses the other ===")
    for key_val in [0, 1]:
        circuit = cirq.Circuit(
            cirq.H(q0), cirq.CNOT(q0, q1),
            cirq.measure(q0, key="a"),
        )
        result = sim.run(circuit, repetitions=100)
        a_counts = result.histogram(key="a")

        sub = cirq.Circuit(
            cirq.H(q0), cirq.CNOT(q0, q1),
            cirq.measure(q0, key="a"),
        )
        print(f"  When q0 measured as |{key_val}⟩, q1 is also |{key_val}⟩")


if __name__ == "__main__":
    main()
