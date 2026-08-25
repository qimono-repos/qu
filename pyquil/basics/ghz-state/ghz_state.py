from pyquil import Program, get_qc
from pyquil.gates import H, CNOT, MEASURE


def ghz_state(n=4):
    p = Program()
    ro = p.declare("ro", "BIT", n)

    p += H(0)
    for i in range(n - 1):
        p += CNOT(i, i + 1)

    for i in range(n):
        p += MEASURE(i, ro[i])

    qc = get_qc(f"{n}q-qvm")
    executable = qc.compile(p)
    results = qc.run(executable).readout_data.get("ro")
    return results


def main():
    results = ghz_state(4)
    print(f"Results shape: {results.shape}")
    counts = {}
    for row in results:
        key = "".join(str(b) for b in row)
        counts[key] = counts.get(key, 0) + 1
    print(f"Counts: {counts}")


if __name__ == "__main__":
    main()
