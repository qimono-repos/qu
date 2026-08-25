#!/usr/bin/env python3
"""Integer factorization using quantum order-finding (RSA threat demo)."""

from __future__ import annotations

import pennylane as qml
import numpy as np
from math import gcd

N_CTRL = 4
N_TARGET = 4
N_TOTAL = N_CTRL + N_TARGET
dev = qml.device("default.qubit", wires=N_TOTAL)


def controlled_mult_by_a(a, power, ctrl_wires, target_wires):
    for _ in range(power):
        for i, tw in enumerate(target_wires):
            qml.ctrl(qml.Pow(qml.PauliX(wires=tw), a), control=ctrl_wires[i])


@qml.qnode(dev)
def period_finding_circuit(a):
    ctrl = list(range(N_CTRL))
    tgt = list(range(N_CTRL, N_TOTAL))

    qml.Hadamard(wires=ctrl)
    qml.PauliX(wires=tgt[0])
    qml.ctrl(controlled_mult_by_a, control=ctrl)(a, 1, ctrl, tgt)
    qml.adjoint(qml.QFT(wires=ctrl))
    return qml.probs(wires=ctrl)


def measure_period(a, n=15):
    probs = period_finding_circuit(a)
    measured = np.argmax(probs)
    if measured == 0:
        return None
    phase = measured / (2**N_CTRL)
    r = int(round(2**N_CTRL * phase))
    if r > 0 and a ** r % n == 1:
        return r
    return None


def factorize(n=15):
    rng = np.random.default_rng(7)
    while True:
        a = int(rng.integers(2, n))
        if gcd(a, n) != 1:
            return a, n // a
        r = measure_period(a, n)
        if r is not None and r % 2 == 0:
            x = pow(a, r // 2, n)
            if x not in (n - 1, 1):
                f1 = gcd(x - 1, n)
                f2 = gcd(x + 1, n)
                if 1 < f1 < n:
                    return f1, n // f1
                if 1 < f2 < n:
                    return f2, n // f2


def main() -> None:
    n = 15
    print(f"RSA threat demo: factor N={n} via order-finding\n")

    a = 7
    print(f"Testing a = {a}:")
    print(qml.draw(period_finding_circuit)(a))
    print()

    probs = period_finding_circuit(a)
    measured = np.argmax(probs)
    phase = measured / (2**N_CTRL)
    print(f"measured output: {measured}  phase ~ {phase:.6f}")
    r = measure_period(a, n)
    if r is not None:
        print(f"recovered period r = {r}")
        print(f"verification: {a}^{r} mod {n} = {pow(a, r, n)}")
    print()

    f1, f2 = factorize(n)
    print(f"{n} = {f1} x {f2}")
    print("This is why RSA needs large keys — quantum computers")
    print("could factor semiprimes in polynomial time.")


if __name__ == "__main__":
    main()
