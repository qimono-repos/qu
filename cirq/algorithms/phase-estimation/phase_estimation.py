"""Quantum Phase Estimation on the T gate, 3 precision qubits."""

import cirq
import numpy as np


def controlled_unitary(
    control: cirq.LineQubit, target: cirq.LineQubit, power: int
) -> list[cirq.Operation]:
    """Return controlled-T^power operations."""
    return [cirq.CPowGate(exponent=power / 8)(control, target)]


def qpe_circuit(
    precision: list[cirq.LineQubit], target: cirq.LineQubit, unitary_power: int = 1
) -> cirq.Circuit:
    """Build the QPE circuit.

    Prepares |1⟩ on target, applies Hadamards to precision qubits,
    controlled unitaries, then inverse QFT on precision register.
    """
    n = len(precision)
    ops: list[cirq.Operation] = []

    ops.append(cirq.X(target))

    for q in precision:
        ops.append(cirq.H(q))

    for i in range(n):
        power = unitary_power * 2 ** (n - 1 - i)
        ops.extend(controlled_unitary(precision[i], target, power))

    for i in range(n // 2):
        ops.append(cirq.SWAP(precision[i], precision[n - 1 - i]))

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            k = j - i
            ops.append(
                cirq.CZPowGate(exponent=-1.0 / (2**k))(precision[j], precision[i])
            )
        ops.append(cirq.H(precision[i]))

    return cirq.Circuit(ops)


def main() -> None:
    n_precision = 3
    precision = cirq.LineQubit.range(n_precision)
    target = cirq.LineQubit(n_precision)
    sim = cirq.Simulator()

    print("=== Quantum Phase Estimation (T gate, 3 precision qubits) ===\n")
    print("T gate: eigenvalue e^(2πi * 1/8) for eigenstate |1⟩\n")

    circuit = qpe_circuit(precision, target, unitary_power=1)
    print("QPE circuit:")
    print(circuit)

    result = sim.simulate(circuit)
    sv = result.final_state_vector

    target_dim = 2
    prec_dim = 2**n_precision
    print("Precision register amplitudes (target traced out):")
    for i in range(prec_dim):
        amp = 0.0
        for t in range(target_dim):
            idx = i * target_dim + t
            amp += abs(sv[idx]) ** 2
        if amp > 1e-6:
            theta_est = i / prec_dim
            phase_est = theta_est * 2 * np.pi
            print(f"  |{i:0{n_precision}b}⟩ → θ ≈ {theta_est:.4f}  (phase ≈ {phase_est:.4f} rad)")

    print("\n=== Expected: θ = 1/8 = 0.125 ===\n")

    print("=== Measuring precision register ===\n")
    meas_circuit = circuit + cirq.measure(*precision, key="prec")
    result = sim.run(meas_circuit, repetitions=1000)
    counts = result.histogram(key="prec")
    for k in sorted(counts):
        theta = k / prec_dim
        print(f"  |{k:0{n_precision}b}⟩: {counts[k]} shots → θ = {theta:.4f}")

    print("\n=== Phase estimation for T² gate (θ = 2/8 = 0.25) ===\n")
    circuit2 = qpe_circuit(precision, target, unitary_power=2)
    result2 = sim.simulate(circuit2)
    sv2 = result2.final_state_vector
    for i in range(prec_dim):
        amp = 0.0
        for t in range(target_dim):
            idx = i * target_dim + t
            amp += abs(sv2[idx]) ** 2
        if amp > 1e-6:
            print(f"  |{i:0{n_precision}b}⟩ → θ ≈ {i / prec_dim:.4f}")


if __name__ == "__main__":
    main()
