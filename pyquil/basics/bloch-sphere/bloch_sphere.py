from pyquil import Program, get_qc
from pyquil.gates import RX, RY, MEASURE
import numpy as np


def single_qubit_rotation(rx_angle: float, ry_angle: float) -> list:
    """Apply RX and RY rotations then measure.

    Args:
        rx_angle: Rotation angle around X-axis in radians.
        ry_angle: Rotation angle around Y-axis in radians.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 1)

    p += RY(ry_angle, 0)
    p += RX(rx_angle, 0)
    p += MEASURE(0, ro[0])

    qc = get_qc("1q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main() -> None:
    rotations = [
        ("|0> (north pole)", 0.0, 0.0),
        ("|1> (south pole)", np.pi, 0.0),
        ("|+> (equator +x)", 0.0, np.pi / 2),
        ("|-> (equator -x)", np.pi, np.pi / 2),
        ("|i> (equator +y)", 0.0, np.pi / 2),
    ]

    for label, rx, ry in rotations:
        results = single_qubit_rotation(rx, ry)
        counts = {}
        for row in results:
            key = "".join(str(b) for b in row)
            counts[key] = counts.get(key, 0) + 1
        print(f"{label}: RX={rx:.4f} RY={ry:.4f} -> {counts}")


if __name__ == "__main__":
    main()
