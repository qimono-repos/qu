"""Quantum Fourier Transform on 3 qubits."""

import cirq
import numpy as np


def qft_circuit(qubits: list[cirq.LineQubit]) -> cirq.Circuit:
    """Build the QFT circuit for the given qubits.

    Uses controlled-Rz rotations and SWAPs.
    """
    n = len(qubits)
    ops: list[cirq.Operation] = []

    for i in range(n):
        ops.append(cirq.H(qubits[i]))
        for j in range(i + 1, n):
            k = j - i
            ops.append(cirq.CZPowGate(exponent=1.0 / (2**k))(qubits[j], qubits[i]))

    ops.extend(cirq.SWAP(qubits[i], qubits[n - 1 - i]) for i in range(n // 2))

    return cirq.Circuit(ops)


def iqft_circuit(qubits: list[cirq.LineQubit]) -> cirq.Circuit:
    """Build the inverse QFT circuit."""
    n = len(qubits)
    ops: list[cirq.Operation] = []

    ops.extend(cirq.SWAP(qubits[i], qubits[n - 1 - i]) for i in range(n // 2))

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            k = j - i
            ops.append(cirq.CZPowGate(exponent=-1.0 / (2**k))(qubits[j], qubits[i]))
        ops.append(cirq.H(qubits[i]))

    return cirq.Circuit(ops)


def main() -> None:
    n = 3
    qubits = cirq.LineQubit.range(n)
    sim = cirq.Simulator()

    print("=== Quantum Fourier Transform (3 qubits) ===\n")

    qft = qft_circuit(qubits)
    print("QFT circuit:")
    print(qft)

    iqft = iqft_circuit(qubits)
    print("Inverse QFT circuit:")
    print(iqft)

    test_states = [
        ("|000⟩", []),
        ("|001⟩", [cirq.X(qubits[2])]),
        ("|101⟩", [cirq.X(qubits[0]), cirq.X(qubits[2])]),
    ]

    for label, prep_ops in test_states:
        print(f"\n--- QFT on {label} ---")
        circuit = cirq.Circuit(prep_ops) + qft
        result = sim.simulate(circuit)
        sv = result.final_state_vector

        for i in range(2**n):
            amp = sv[i]
            if abs(amp) > 1e-6:
                print(f"  |{i:0{n}b}⟩: {amp:.4f}")

    print("\n=== QFT as matrix ===\n")
    qft_matrix = np.array(qft.unitary())
    print("QFT unitary (8×8):")
    print(np.array2string(qft_matrix, precision=3, suppress_small=True))

    print("\n=== Roundtrip: QFT then IQFT ===\n")
    q0, q1, q2 = cirq.LineQubit.range(3)
    original = cirq.Circuit(cirq.X(q0), cirq.X(q2))
    print(f"Original state |101⟩:")
    sv_orig = sim.simulate(original).final_state_vector
    print(f"  {np.array2string(sv_orig, precision=3)}")

    roundtrip = original + qft + iqft
    sv_rt = sim.simulate(roundtrip).final_state_vector
    print(f"After QFT → IQFT:")
    print(f"  {np.array2string(sv_rt, precision=3)}")


if __name__ == "__main__":
    main()
