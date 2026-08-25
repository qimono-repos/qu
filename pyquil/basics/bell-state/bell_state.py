from pyquil import Program, get_qc
from pyquil.gates import H, CNOT, MEASURE
from pyquil.quilbase import Declare


def bell_state():
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


def main():
    results = bell_state()
    print(f"Results: {results}")
    counts = {}
    for row in results:
        key = "".join(str(b) for b in row)
        counts[key] = counts.get(key, 0) + 1
    print(f"Counts: {counts}")


if __name__ == "__main__":
    main()
