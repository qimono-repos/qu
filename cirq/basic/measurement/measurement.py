"""Measurement in Z and X bases with statistics over 1000 repetitions."""

import numpy as np
import cirq


def main() -> None:
    q = cirq.LineQubit(0)
    sim = cirq.Simulator()
    reps = 1000

    print("=== Measurement in the Z (computational) basis ===\n")

    z_circuits: dict[str, cirq.Circuit] = {
        "H|0⟩ → Z-meas": cirq.Circuit(cirq.H(q), cirq.measure(q, key="m")),
        "H|1⟩ → Z-meas": cirq.Circuit(cirq.X(q), cirq.H(q), cirq.measure(q, key="m")),
    }

    for label, circuit in z_circuits.items():
        result = sim.run(circuit, repetitions=reps)
        counts = result.histogram(key="m")
        print(f"{label}: {dict(sorted(counts.items()))}")

    print("\n=== Measurement in the X basis ===")
    print("(Apply H before measuring to switch to X basis)\n")

    # To measure in X basis, apply H before measurement.
    # |+⟩ has eigenvalue +1 for X, so measuring |+⟩ in X gives 0.
    # |−⟩ has eigenvalue -1 for X, so measuring |−⟩ in X gives 1.
    x_circuits: dict[str, cirq.Circuit] = {
        "|+⟩ → X-meas": cirq.Circuit(cirq.H(q), cirq.H(q), cirq.measure(q, key="m")),
        "|-⟩ → X-meas": cirq.Circuit(cirq.X(q), cirq.H(q), cirq.H(q), cirq.measure(q, key="m")),
    }

    for label, circuit in x_circuits.items():
        result = sim.run(circuit, repetitions=reps)
        counts = result.histogram(key="m")
        print(f"{label}: {dict(sorted(counts.items()))}")

    print("\n=== Partially rotated state: Ry(π/4)|0⟩ ===\n")

    ry_circuit = cirq.Circuit(cirq.ry(np.pi / 4)(q), cirq.measure(q, key="m"))
    result = sim.run(ry_circuit, repetitions=reps)
    counts = result.histogram(key="m")
    p1 = counts.get(1, 0) / reps
    print(f"  Z-basis: {dict(sorted(counts.items()))}  (P(|1⟩) ≈ {p1:.3f}, ideal = sin²(π/8) ≈ {np.sin(np.pi/8)**2:.3f})")

    x_circuit = cirq.Circuit(cirq.ry(np.pi / 4)(q), cirq.H(q), cirq.measure(q, key="m"))
    result = sim.run(x_circuit, repetitions=reps)
    counts = result.histogram(key="m")
    print(f"  X-basis: {dict(sorted(counts.items()))}")

    print("\n=== State vector for reference ===")
    sv = sim.simulate(cirq.Circuit(cirq.ry(np.pi / 4)(q))).final_state_vector
    print(f"  Ry(π/4)|0⟩ = {np.array2string(sv, precision=4)}")


if __name__ == "__main__":
    main()
