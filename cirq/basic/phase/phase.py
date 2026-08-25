"""Global and relative phase via state vector inspection."""

import numpy as np
import cirq


def main() -> None:
    q = cirq.LineQubit(0)
    sim = cirq.Simulator()

    print("=== Global Phase ===")
    print("Global phase is unobservable in quantum mechanics.\n")
    print("Compare |0⟩ with e^{iθ}|0⟩ — same measurement statistics.\n")

    for theta_label, theta_val in [("θ=0", 0), ("θ=π/4", np.pi / 4), ("θ=π/2", np.pi / 2)]:
        circuit = cirq.Circuit([cirq.GlobalPhaseGate(theta_val)])
        result = sim.simulate(circuit)
        sv = result.final_state_vector
        print(f"  GlobalPhaseGate({theta_label}): state = {sv}")

    print("\n=== Relative Phase ===\n")

    print("--- |0⟩ vs |1⟩ ---")
    for label, ops in [("|0⟩", []), ("|1⟩", [cirq.X(q)])]:
        result = sim.simulate(cirq.Circuit(ops))
        print(f"  {label}: {result.final_state_vector}")

    print("\n--- |+⟩ vs |-⟩ (Hadamard basis) ---")
    for label, ops in [("|+⟩ = H|0⟩", [cirq.H(q)]), ("|-⟩ = XH|0⟩", [cirq.X(q), cirq.H(q)])]:
        result = sim.simulate(cirq.Circuit(ops))
        sv = result.final_state_vector
        print(f"  {label}: {np.array2string(sv, precision=4)}")

    print("\n--- Effect of S gate (adds π/2 relative phase) ---")
    for label, ops in [
        ("S|+⟩", [cirq.H(q), cirq.S(q)]),
        ("S|-⟩", [cirq.X(q), cirq.H(q), cirq.S(q)]),
    ]:
        result = sim.simulate(cirq.Circuit(ops))
        sv = result.final_state_vector
        print(f"  {label}: {np.array2string(sv, precision=4)}")

    print("\n--- Measurement is phase-insensitive ---")
    for label, ops in [("S|+⟩", [cirq.H(q), cirq.S(q)]), ("|-⟩", [cirq.X(q), cirq.H(q)])]:
        circuit = cirq.Circuit(ops + [cirq.measure(q, key="m")])
        result = sim.run(circuit, repetitions=20)
        print(f"  {label} meas: {result.histogram(key='m')}")


if __name__ == "__main__":
    main()
