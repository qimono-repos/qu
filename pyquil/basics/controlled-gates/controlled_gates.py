from pyquil import Program, get_qc
from pyquil.gates import CNOT, CZ, H, MEASURE


def cnot_demo() -> list:
    """Apply H on control then CNOT and measure both qubits.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 2)

    p += H(0)
    p += CNOT(0, 1)
    p += MEASURE(0, ro[0])
    p += MEASURE(1, ro[1])

    qc = get_qc("2q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def cz_demo() -> list:
    """Apply H on both qubits then CZ and measure.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 2)

    p += H(0)
    p += H(1)
    p += CZ(0, 1)
    p += MEASURE(0, ro[0])
    p += MEASURE(1, ro[1])

    qc = get_qc("2q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main() -> None:
    cnot_results = cnot_demo()
    cnot_counts = {}
    for row in cnot_results:
        key = "".join(str(b) for b in row)
        cnot_counts[key] = cnot_counts.get(key, 0) + 1
    print(f"CNOT (H on control) -> {cnot_counts}")

    cz_results = cz_demo()
    cz_counts = {}
    for row in cz_results:
        key = "".join(str(b) for b in row)
        cz_counts[key] = cz_counts.get(key, 0) + 1
    print(f"CZ (H on both) -> {cz_counts}")


if __name__ == "__main__":
    main()
