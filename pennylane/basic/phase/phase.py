#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)


@qml.qnode(dev)
def with_phase(angle: float) -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.RZ(angle, wires=0)
    return qml.state()


@qml.qnode(dev)
def control_phase(a: float, b: float) -> qml.typing.Result:
    qml.Hadamard(wires=0)
    qml.PhaseShift(a, wires=0)
    qml.Hadamard(wires=0)
    qml.PhaseShift(b, wires=0)
    return qml.state()


def relative_phase(state_vec: np.ndarray) -> float:
    """Extract the relative phase between |0> and |1> amplitudes."""
    amp_0, amp_1 = state_vec
    if abs(amp_0) < 1e-10:
        return 0.0
    return float(np.angle(amp_1 / amp_0))


def main() -> None:
    print("=== Phase Shifts ===")
    print()
    print("Starting from H|0> = (|0> + |1>)/sqrt(2),")
    print("applying RZ(theta) rotates the relative phase by theta.")
    print()

    for angle in [0.0, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2]:
        sv = with_phase(angle)
        rp = relative_phase(sv)
        probs = np.abs(sv) ** 2
        print(f"  RZ({angle:.4f}):  rel phase = {rp:.4f} rad ({np.degrees(rp):.1f} deg),  "
              f"P(|0>) = {probs[0]:.4f},  P(|1>) = {probs[1]:.4f}")

    print()
    print("=== Phase Accumulation ===")
    print()
    print("Two successive phase shifts add their phases.")
    sv = control_phase(np.pi / 3, np.pi / 6)
    rp = relative_phase(sv)
    print(f"  H -> PS(pi/3) -> H -> PS(pi/6):  rel phase = {rp:.4f} rad ({np.degrees(rp):.1f} deg)")
    print(f"  Expected total phase: {np.pi / 3 + np.pi / 6:.4f} rad ({np.degrees(np.pi / 3 + np.pi / 6):.1f} deg)")


if __name__ == "__main__":
    main()
