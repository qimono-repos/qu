#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)


@qml.qnode(dev)
def state_after_rotations(rx: float, ry: float, rz: float) -> qml.typing.Result:
    qml.RX(rx, wires=0)
    qml.RY(ry, wires=0)
    qml.RZ(rz, wires=0)
    return qml.state()


def state_to_bloch(state_vec: np.ndarray) -> tuple[float, float, float]:
    """Convert a single-qubit state vector to Bloch sphere coordinates (x, y, z)."""
    rho = np.outer(state_vec, np.conj(state_vec))
    x = 2 * np.real(rho[0, 1])
    y = 2 * np.imag(rho[1, 0])
    z = np.real(rho[0, 0] - rho[1, 1])
    return (float(x), float(y), float(z))


def main() -> None:
    print("=== Bloch Sphere from Single-Qubit Rotations ===")
    print()
    print("Bloch coordinates: x = <X>, y = <Y>, z = <Z>")
    print("Point (0, 0, 1) = |0>,  (0, 0, -1) = |1>,  (1, 0, 0) = |+>")
    print()

    rotations = [
        ("|0> (no rotation)", 0.0, 0.0, 0.0),
        ("|1> (X gate)", np.pi, 0.0, 0.0),
        ("|+> (Y rotation)", 0.0, np.pi / 2, 0.0),
        ("|-> (Y then X)", 0.0, -np.pi / 2, 0.0),
        ("RZ(pi/4) on |+>", 0.0, np.pi / 2, np.pi / 4),
        ("RZ(pi/2) on |+>", 0.0, np.pi / 2, np.pi / 2),
        ("|i> (S gate)", 0.0, np.pi / 2, np.pi / 2),
    ]

    for label, rx, ry, rz in rotations:
        sv = state_after_rotations(rx, ry, rz)
        bx, by, bz = state_to_bloch(sv)
        print(f"  {label:25s}  ->  ({bx:+.4f}, {by:+.4f}, {bz:+.4f})")

    print()
    print("=== Equator Walk (pure phase rotations) ===")
    print()
    print("Applying RZ to |+> walks along the equator (z=0).")
    for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        sv = state_after_rotations(0.0, np.pi / 2, angle)
        bx, by, bz = state_to_bloch(sv)
        print(f"  RZ({angle:.2f}) on |+>:  ({bx:+.4f}, {by:+.4f}, {bz:+.4f})")


if __name__ == "__main__":
    main()
