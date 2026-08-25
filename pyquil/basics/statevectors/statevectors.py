from pyquil import Program, get_qc
from pyquil.gates import H, MEASURE


def plus_state() -> list:
    """Prepare |+> = (|0> + |1>)/sqrt(2) and measure.

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


def main() -> None:
    results = plus_state()
    counts = {}
    for row in results:
        key = "".join(str(b) for b in row)
        counts[key] = counts.get(key, 0) + 1
    print(f"|+> state measurement counts: {counts}")
    print("Expect ~50/50 split between |0> and |1>")


if __name__ == "__main__":
    main()
