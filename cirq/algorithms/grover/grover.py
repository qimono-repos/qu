"""Grover's search algorithm on 3 qubits (N=8)."""

import cirq
import numpy as np


def grover_oracle(
    qubits: list[cirq.LineQubit], target: int
) -> list[cirq.Operation]:
    """Oracle that marks the target state with a phase flip.

    Uses multi-controlled Z (decomposed as CCX + CZ + CCX).
    """
    n = len(qubits)
    target_binary = format(target, f"0{n}b")
    ops: list[cirq.Operation] = []

    for i, bit in enumerate(reversed(target_binary)):
        if bit == "0":
            ops.append(cirq.X(qubits[i]))

    if n == 2:
        ops.append(cirq.CZ(qubits[0], qubits[1]))
    else:
        ops.append(cirq.CCX(qubits[0], qubits[1], qubits[2]))
        ops.append(cirq.CZ(qubits[2], qubits[1]))
        ops.append(cirq.CCX(qubits[0], qubits[1], qubits[2]))

    for i, bit in enumerate(reversed(target_binary)):
        if bit == "0":
            ops.append(cirq.X(qubits[i]))

    return ops


def diffusion_operator(qubits: list[cirq.LineQubit]) -> list[cirq.Operation]:
    """Grover diffusion operator: 2|s><s| - I where |s> = H^n|0>^n."""
    n = len(qubits)
    ops: list[cirq.Operation] = []

    ops.extend(cirq.H(q) for q in qubits)
    ops.extend(cirq.X(q) for q in qubits)

    if n == 2:
        ops.append(cirq.CZ(qubits[0], qubits[1]))
    else:
        ops.append(cirq.CCX(qubits[0], qubits[1], qubits[2]))
        ops.append(cirq.CZ(qubits[2], qubits[1]))
        ops.append(cirq.CCX(qubits[0], qubits[1], qubits[2]))

    ops.extend(cirq.X(q) for q in qubits)
    ops.extend(cirq.H(q) for q in qubits)

    return ops


def main() -> None:
    n = 3
    N = 2**n
    qubits = cirq.LineQubit.range(n)
    target = 5
    sim = cirq.Simulator()

    num_iterations = int(np.pi / 4 * np.sqrt(N))
    print(f"=== Grover Search (N={N}, target=|{target:0{n}b}>) ===\n")
    print(f"Ideal iterations: {num_iterations}\n")

    print("Circuit:")
    circuit = cirq.Circuit(
        [cirq.H(q) for q in qubits],
        num_iterations
        * (
            grover_oracle(qubits, target)
            + diffusion_operator(qubits)
        ),
    )
    print(circuit)

    result = sim.simulate(circuit)
    sv = result.final_state_vector
    probs = np.abs(sv) ** 2

    print("\nFinal probabilities:")
    for i in range(N):
        marker = " <-- target" if i == target else ""
        print(f"  |{i:0{n}b}⟩: {probs[i]:.4f}{marker}")

    print(f"\nP(target) = {probs[target]:.4f} (ideal: ~1.000)\n")

    print("=== Measurement statistics (1000 shots) ===\n")
    meas_circuit = cirq.Circuit(
        [cirq.H(q) for q in qubits],
        num_iterations
        * (
            grover_oracle(qubits, target)
            + diffusion_operator(qubits)
        ),
        cirq.measure(*qubits, key="m"),
    )
    result = sim.run(meas_circuit, repetitions=1000)
    counts = result.histogram(key="m")
    for k in sorted(counts):
        print(f"  |{k:0{n}b}⟩: {counts[k]} ({counts[k] / 10:.1f}%)")

    print("\n=== Iteration count sweep ===\n")
    for iters in range(6):
        sweep = cirq.Circuit(
            [cirq.H(q) for q in qubits],
            iters * (grover_oracle(qubits, target) + diffusion_operator(qubits)),
        )
        sv = sim.simulate(sweep).final_state_vector
        p = abs(sv[target]) ** 2
        print(f"  {iters} iterations: P(target) = {p:.4f}")


if __name__ == "__main__":
    main()
