"""Computational basis states: |0⟩ and |1⟩ with measurement."""

import cirq


def main() -> None:
    q = cirq.LineQubit(0)

    # |0⟩ state (default)
    circuit_zero = cirq.Circuit(cirq.measure(q, key="m"))
    result_zero = cirq.Simulator().simulate(circuit_zero)
    print("=== |0⟩ state ===")
    print(circuit_zero)

    sim = cirq.Simulator()
    for state in ("|0⟩", "|1⟩"):
        if state == "|0⟩":
            circuit = cirq.Circuit(cirq.measure(q, key="m"))
        else:
            circuit = cirq.Circuit(cirq.X(q), cirq.measure(q, key="m"))

        result = sim.run(circuit, repetitions=20)
        counts = result.histogram(key="m")
        print(f"\n{state} measurement counts (20 shots):")
        for k in sorted(counts):
            label = f"|{k}⟩"
            print(f"  {label}: {counts[k]}")

    print("\nCircuit diagrams:")
    print("  |0⟩:", cirq.Circuit(cirq.measure(q, key="m")), sep="\n")
    print("  |1⟩:", cirq.Circuit(cirq.X(q), cirq.measure(q, key="m")), sep="\n")


if __name__ == "__main__":
    main()
