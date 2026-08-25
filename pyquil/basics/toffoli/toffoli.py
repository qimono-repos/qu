from pyquil import Program, get_qc
from pyquil.gates import CCNOT, H, MEASURE


def toffoli_demo() -> list:
    """Apply Toffoli (CCNOT) gate on 3 qubits and measure.

    Sets qubits 0 and 1 to |1>, applies CCNOT to flip qubit 2.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 3)

    from pyquil.gates import X
    p += X(0)
    p += X(1)
    p += CCNOT(0, 1, 2)
    for i in range(3):
        p += MEASURE(i, ro[i])

    qc = get_qc("3q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def toffoli_with_superposition() -> list:
    """Put control qubits in superposition, apply Toffoli, measure.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 3)

    p += H(0)
    p += H(1)
    p += CCNOT(0, 1, 2)
    for i in range(3):
        p += MEASURE(i, ro[i])

    qc = get_qc("3q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main() -> None:
    results = toffoli_demo()
    counts = {}
    for row in results:
        key = "".join(str(b) for b in row)
        counts[key] = counts.get(key, 0) + 1
    print(f"Toffoli |110> input -> {counts}")

    results = toffoli_with_superposition()
    counts = {}
    for row in results:
        key = "".join(str(b) for b in row)
        counts[key] = counts.get(key, 0) + 1
    print(f"Toffoli with superposition -> {counts}")


if __name__ == "__main__":
    main()
