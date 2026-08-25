"""Bloch sphere: single-qubit rotations and state visualization."""

import numpy as np
import cirq


def bloch_components(state_vector: np.ndarray) -> tuple[float, float, float]:
    """Extract Bloch sphere (x, y, z) from a single-qubit state vector."""
    rho = np.outer(state_vector, np.conj(state_vector))
    x = 2 * rho[0, 1].real
    y = 2 * rho[0, 1].imag
    z = rho[0, 0].real - rho[1, 1].real
    return (x, y, z)


def main() -> None:
    q = cirq.LineQubit(0)
    sim = cirq.Simulator()

    rotations: dict[str, list[cirq.Operation]] = {
        "|0⟩ (north pole)": [],
        "|1⟩ (south pole)": [cirq.X(q)],
        "|+⟩ (east)": [cirq.H(q)],
        "|-⟩ (west)": [cirq.X(q), cirq.H(q)],
        "|+i⟩ (front)": [cirq.H(q), cirq.S(q)],
        "|-i⟩ (back)": [cirq.X(q), cirq.H(q), cirq.S(q)],
        "Rx(π/2)|0⟩": [cirq.rx(np.pi / 2)(q)],
        "Ry(π/2)|0⟩": [cirq.ry(np.pi / 2)(q)],
        "Rz(π/4)|+⟩": [cirq.H(q), cirq.rz(np.pi / 4)(q)],
    }

    print("=== Bloch Sphere Positions ===\n")
    print(f"{'State':<22} {'x':>7} {'y':>7} {'z':>7}")
    print("-" * 48)

    for label, ops in rotations.items():
        result = sim.simulate(cirq.Circuit(ops))
        sv = result.final_state_vector
        x, y, z = bloch_components(sv)
        print(f"{label:<22} {x:7.4f} {y:7.4f} {z:7.4f}")

    print("\n=== Rotating |0⟩ around each axis ===\n")
    for axis_name, rot_gate in [("X", cirq.rx), ("Y", cirq.ry), ("Z", cirq.rz)]:
        angles = [np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2]
        print(f"  {axis_name}-axis rotations:")
        for angle in angles:
            result = sim.simulate(cirq.Circuit(rot_gate(angle)(q)))
            sv = result.final_state_vector
            x, y, z = bloch_components(sv)
            print(f"    θ={angle:.2f} → ({x:.3f}, {y:.3f}, {z:.3f})")


if __name__ == "__main__":
    main()
