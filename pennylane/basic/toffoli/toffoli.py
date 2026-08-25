#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=3)


@qml.qnode(dev)
def toffoli_000() -> qml.typing.Result:
    qml.Toffoli(wires=[0, 1, 2])
    return qml.state()


@qml.qnode(dev)
def toffoli_110() -> qml.typing.Result:
    qml.PauliX(wires=0)
    qml.PauliX(wires=1)
    qml.Toffoli(wires=[0, 1, 2])
    return qml.state()


@qml.qnode(dev)
def toffoli_100() -> qml.typing.Result:
    qml.PauliX(wires=0)
    qml.Toffoli(wires=[0, 1, 2])
    return qml.state()


@qml.qnode(dev)
def toffoli_all_inputs() -> qml.typing.Result:
    return qml.probs(wires=[0, 1, 2])


def main() -> None:
    print("=== Toffoli (CCX) Gate — 3-Qubit Demonstration ===")
    print()
    print("Toffoli flips target (q2) only when both controls (q0, q1) are |1>.")
    print("Truth table: |c0 c1 t> -> |c0 c1 (t XOR (c0 AND c1))>")
    print()

    print("--- Individual Cases ---")
    print()

    cases = [
        ("|000> -> |000>", toffoli_000),
        ("|110> -> |111> (both controls=1, target flips)", toffoli_110),
        ("|100> -> |100> (only one control=1, no flip)", toffoli_100),
    ]

    for label, fn in cases:
        sv = fn()
        probs = np.abs(sv) ** 2
        outcome = np.argmax(probs)
        bits = format(outcome, "03b")
        print(f"  {label}")
        print(f"    state: {sv}")
        print(f"    dominant: |{bits}> (p = {probs[outcome]:.4f})")
        print()

    print("--- Full Truth Table (probabilities) ---")
    print()
    sv = toffoli_all_inputs()
    probs = np.abs(sv) ** 2
    print(f"  {'Input':>8s}  {'Output':>8s}  {'P(output)':>10s}")
    print(f"  {'-'*8}  {'-'*8}  {'-'*10}")
    for i in range(8):
        inp = format(i, "03b")
        # Toffoli: flip bit 2 if bits 0 and 1 are both 1
        c0 = (i >> 2) & 1
        c1 = (i >> 1) & 1
        t = i & 1
        out_t = t ^ (c0 & c1)
        out = (c0 << 2) | (c1 << 1) | out_t
        out_bits = format(out, "03b")
        print(f"  |{inp}>  ->  |{out_bits}>  {probs[i]:.4f}")

    print()
    print("--- Toffoli as Quantum AND Gate ---")
    print()
    print("Initialize q2 in |1> (ancilla), Toffoli computes AND into q2:")
    print()

    dev_and = qml.device("default.qubit", wires=3)

    @qml.qnode(dev_and)
    def quantum_and(a: int, b: int) -> qml.typing.Result:
        if a:
            qml.PauliX(wires=0)
        if b:
            qml.PauliX(wires=1)
        qml.PauliX(wires=2)
        qml.Toffoli(wires=[0, 1, 2])
        return qml.probs(wires=2)

    for a in [0, 1]:
        for b in [0, 1]:
            p = quantum_and(a, b)
            print(f"  AND({a}, {b}) = {np.argmax(p)}")


if __name__ == "__main__":
    main()
