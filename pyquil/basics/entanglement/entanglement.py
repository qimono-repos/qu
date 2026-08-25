from pyquil import Program, get_qc
from pyquil.gates import H, CNOT, MEASURE


def bell_pair() -> list:
    """Create a Bell pair and measure both qubits.

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


def ghz_3qubit() -> list:
    """Create a 3-qubit GHZ state and measure all qubits.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 3)

    p += H(0)
    p += CNOT(0, 1)
    p += CNOT(1, 2)
    for i in range(3):
        p += MEASURE(i, ro[i])

    qc = get_qc("3q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main() -> None:
    bell_results = bell_pair()
    bell_counts = {}
    for row in bell_results:
        key = "".join(str(b) for b in row)
        bell_counts[key] = bell_counts.get(key, 0) + 1
    print(f"Bell pair: {bell_counts}")

    ghz_results = ghz_3qubit()
    ghz_counts = {}
    for row in ghz_results:
        key = "".join(str(b) for b in row)
        ghz_counts[key] = ghz_counts.get(key, 0) + 1
    print(f"3-qubit GHZ: {ghz_counts}")


if __name__ == "__main__":
    main()
