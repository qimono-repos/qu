import cudaq
import numpy as np


@cudaq.kernel
def phase_kernel(angle: float):
    qubit = cudaq.qvector(1)
    h(qubit[0])
    rz(angle, qubit[0])


if __name__ == "__main__":
    angles = [0.0, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2]
    for angle in angles:
        sv = cudaq.get_state(phase_kernel, angle)
        amps = np.array(sv)
        print(f"Phase = {angle:.4f} rad ({np.degrees(angle):.1f} deg):  "
              f"|0>={amps[0]:+.4f}  |1>={amps[1]:+.4f}")
