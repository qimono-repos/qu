"""Oracle basics: a simple oracle marking the |11⟩ state with a phase flip."""

import cirq
import numpy as np


def oracle_mark_11(q0: cirq.LineQubit, q1: cirq.LineQubit) -> list[cirq.Operation]:
    """Oracle that flips the phase of |11⟩.

    CZ(q0, q1) applies a -1 phase to |11⟩ and leaves other states unchanged.
    """
    return [cirq.CZ(q0, q1)]


def main() -> None:
    q0, q1 = cirq.LineQubit.range(2)
    sim = cirq.Simulator()

    print("=== Oracle marking |11⟩ ===\n")
    circuit = cirq.Circuit(oracle_mark_11(q0, q1))
    print(circuit)

    print("Truth table (oracle output state):")
    print(f"{'Input':<10} {'State Vector'}")
    print("-" * 50)
    for a in range(2):
        for b in range(2):
            ops: list[cirq.Operation] = []
            if a:
                ops.append(cirq.X(q0))
            if b:
                ops.append(cirq.X(q1))
            ops.extend(oracle_mark_11(q0, q1))
            result = sim.simulate(cirq.Circuit(ops))
            sv = result.final_state_vector
            print(f"|{a}{b}⟩       {np.array2string(sv, precision=3)}")

    print("\n=== Using oracle in a search circuit ===\n")
    search = cirq.Circuit(
        cirq.H(q0),
        cirq.H(q1),
        *oracle_mark_11(q0, q1),
        cirq.H(q0),
        cirq.H(q1),
    )
    print(search)

    result = sim.simulate(search)
    sv = result.final_state_vector
    probs = np.abs(sv) ** 2
    for i in range(4):
        print(f"  P(|{i:02b}⟩) = {probs[i]:.4f}")

    print("\n=== Amplitude after oracle on superposition ===\n")
    prep = cirq.Circuit(cirq.H(q0), cirq.H(q1), *oracle_mark_11(q0, q1))
    result = sim.simulate(prep)
    sv = result.final_state_vector
    for i in range(4):
        print(f"  |{i:02b}⟩: amplitude = {sv[i]:.4f},  prob = {abs(sv[i])**2:.4f}")


if __name__ == "__main__":
    main()
