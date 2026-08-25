from pyquil import Program, get_qc
from pyquil.gates import H, MEASURE


def tensor_product_state() -> list:
    """Prepare |+> tensor |0> on two qubits and measure.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 2)

    p += H(0)
    p += MEASURE(0, ro[0])
    p += MEASURE(1, ro[1])

    qc = get_qc("2q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main() -> None:
    results = tensor_product_state()
    counts = {}
    for row in results:
        key = "".join(str(b) for b in row)
        counts[key] = counts.get(key, 0) + 1
    print(f"|+> tensor |0> counts: {counts}")
    print("Expect |00> and |10> only (qubit 0 in superposition, qubit 1 in |0>)")


if __name__ == "__main__":
    main()
