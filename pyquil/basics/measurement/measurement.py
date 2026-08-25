from pyquil import Program, get_qc
from pyquil.gates import H, MEASURE


def measure_in_z_basis() -> list:
    """Measure |+> in the Z (computational) basis.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 1)

    p += H(0)
    p += MEASURE(0, ro[0])

    qc = get_qc("1q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def measure_in_x_basis() -> list:
    """Measure |0> in the X basis by applying H before measurement.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 1)

    p += H(0)
    p += H(0)
    p += MEASURE(0, ro[0])

    qc = get_qc("1q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main() -> None:
    z_results = measure_in_z_basis()
    z_counts = {}
    for row in z_results:
        key = "".join(str(b) for b in row)
        z_counts[key] = z_counts.get(key, 0) + 1
    print(f"|+> measured in Z basis: {z_counts}")

    x_results = measure_in_x_basis()
    x_counts = {}
    for row in x_results:
        key = "".join(str(b) for b in row)
        x_counts[key] = x_counts.get(key, 0) + 1
    print(f"|0> measured in X basis (H-H): {x_counts}")


if __name__ == "__main__":
    main()
