from pyquil import Program, get_qc
from pyquil.gates import X, Y, Z, H, S, T, MEASURE


def apply_gate(gate_fn, label: str) -> list:
    """Apply a single-qubit gate and measure.

    Args:
        gate_fn: A callable that takes a qubit index and returns a gate instruction.
        label: Name of the gate for display.

    Returns:
        Array of measurement results.
    """
    p = Program()
    ro = p.declare("ro", "BIT", 1)

    p += gate_fn(0)
    p += MEASURE(0, ro[0])

    qc = get_qc("1q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main() -> None:
    gates = [
        ("X", X),
        ("Y", Y),
        ("Z", Z),
        ("H", H),
        ("S", S),
        ("T", T),
    ]

    for label, gate_fn in gates:
        results = apply_gate(gate_fn, label)
        counts = {}
        for row in results:
            key = "".join(str(b) for b in row)
            counts[key] = counts.get(key, 0) + 1
        print(f"{label} gate -> Counts: {counts}")


if __name__ == "__main__":
    main()
