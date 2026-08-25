import cudaq
import numpy as np


@cudaq.kernel
def rx_rotation(theta: float):
    qubit = cudaq.qvector(1)
    rx(theta, qubit[0])


@cudaq.kernel
def ry_rotation(theta: float):
    qubit = cudaq.qvector(1)
    ry(theta, qubit[0])


@cudaq.kernel
def rz_rotation(theta: float):
    qubit = cudaq.qvector(1)
    h(qubit[0])
    rz(theta, qubit[0])


def bloch_coords(amps: np.ndarray) -> tuple[float, float, float]:
    x = 2.0 * np.real(np.conj(amps[0]) * amps[1])
    y = 2.0 * np.imag(np.conj(amps[1]) * amps[0])
    z = float(np.abs(amps[0]) ** 2 - np.abs(amps[1]) ** 2)
    return x, y, z


if __name__ == "__main__":
    thetas = [0.0, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]

    print("=== Rx rotations ===")
    for t in thetas:
        sv = np.array(cudaq.get_state(rx_rotation, t))
        x, y, z = bloch_coords(sv)
        print(f"  Rx({np.degrees(t):6.1f} deg) -> ({x:+.4f}, {y:+.4f}, {z:+.4f})")

    print("\n=== Ry rotations ===")
    for t in thetas:
        sv = np.array(cudaq.get_state(ry_rotation, t))
        x, y, z = bloch_coords(sv)
        print(f"  Ry({np.degrees(t):6.1f} deg) -> ({x:+.4f}, {y:+.4f}, {z:+.4f})")

    print("\n=== Rz rotations (after Hadamard) ===")
    for t in thetas:
        sv = np.array(cudaq.get_state(rz_rotation, t))
        x, y, z = bloch_coords(sv)
        print(f"  Rz({np.degrees(t):6.1f} deg) -> ({x:+.4f}, {y:+.4f}, {z:+.4f})")
