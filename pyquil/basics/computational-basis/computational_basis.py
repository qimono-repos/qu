from pyquil import Program, get_qc
from pyquil.gates import X, MEASURE


def computational_basis(state: int) -> list:
    """Prepare a single qubit in |0> or |1> and measure.

    Args:
        state: 0 for |0>, 1 for |1>.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 1)

    if state == 1:
        p += X(0)

    p += MEASURE(0, ro[0])

    qc = get_qc("1q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main() -> None:
    for state in [0, 1]:
        results = computational_basis(state)
        counts = {}
        for row in results:
            key = "".join(str(b) for b in row)
            counts[key] = counts.get(key, 0) + 1
        print(f"|{state}> -> Counts: {counts}")


if __name__ == "__main__":
    main()
