from pyquil import Program, get_qc
from pyquil.gates import H, MEASURE


def superposition_circuit() -> list:
    """Put a qubit in superposition with Hadamard and measure.

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
    n_shots = 1000
    results = superposition_circuit()
    counts = {}
    for row in results:
        key = "".join(str(b) for b in row)
        counts[key] = counts.get(key, 0) + 1
    print(f"Superposition measurement ({n_shots} shots): {counts}")
    print("H|0> should yield ~50% |0> and ~50% |1>")


if __name__ == "__main__":
    main()
