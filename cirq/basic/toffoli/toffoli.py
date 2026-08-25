"""Toffoli (CCX) gate: 3-qubit truth table."""

import numpy as np
import cirq


def main() -> None:
    q0, q1, q2 = cirq.LineQubit.range(3)
    sim = cirq.Simulator()

    print("=== Toffoli (CCX) Gate ===\n")
    print(f"Circuit: {cirq.Circuit(cirq.CCX(q0, q1, q2))}\n")

    print(f"Matrix ({2**3}x{2**3}):")
    print(np.array2string(np.array(cirq.CCX.unitary()), precision=0))
    print()

    print("=== 3-Qubit Truth Table ===\n")
    print(f"{'Input':<12} {'Output':<12} {'State Vector'}")
    print("-" * 60)

    for a in range(2):
        for b in range(2):
            for c in range(2):
                ops: list[cirq.Operation] = []
                if a:
                    ops.append(cirq.X(q0))
                if b:
                    ops.append(cirq.X(q1))
                if c:
                    ops.append(cirq.X(q2))
                ops.append(cirq.CCX(q0, q1, q2))

                result = sim.simulate(cirq.Circuit(ops))
                sv = result.final_state_vector
                out_state = np.argmax(np.abs(sv))
                out_binary = format(out_state, "03b")
                print(f"|{a}{b}{c}⟩         |{out_binary}⟩         {np.array2string(sv, precision=3)}")

    print("\n=== Key observation ===")
    print("The Toffoli flips q2 (target) only when both q0 and q1 (controls) are |1⟩.")
    print("It is universal for classical reversible computation.")

    print("\n=== Toffoli as decomposition building block ===")
    print("CCX can be decomposed into H, T, CNOT, and T† gates.")
    toffoli_decomp = cirq.Circuit(
        cirq.H(q2),
        cirq.CNOT(q1, q2),
        cirq.T(q2) ** -1,
        cirq.CNOT(q0, q2),
        cirq.T(q2),
        cirq.CNOT(q1, q2),
        cirq.T(q2) ** -1,
        cirq.CNOT(q0, q2),
        cirq.T(q1),
        cirq.T(q2),
        cirq.H(q2),
        cirq.CNOT(q0, q1),
        cirq.T(q0),
        cirq.T(q1) ** -1,
        cirq.CNOT(q0, q1),
    )
    print(f"\nDecomposed circuit ({len(toffoli_decomp)} operations):")
    print(toffoli_decomp)


if __name__ == "__main__":
    main()
