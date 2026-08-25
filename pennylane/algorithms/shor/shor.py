#!/usr/bin/env python3
"""Shor's algorithm — factoring 15 using quantum order finding.

This demonstrates the quantum subroutine.  The classical pre/post-processing
(random choice of a, GCD, continued fractions) is done with numpy.
"""
import pennylane as qml
import numpy as np
from math import gcd

N = 15
N_PREC = 4
N_TARGET = 4
N_TOTAL = N_PREC + N_TARGET
dev = qml.device("default.qubit", wires=N_TOTAL)


def controlled_mult_mod18(power: int) -> None:
    """Controlled multiplication by a^power mod 18 on 4 target qubits.

    Uses the convention: target register holds values 0–15 in binary,
    with an extra qubit for overflow (mod 18 arithmetic).
    """
    a = 7
    a_pow = pow(a, power, 18)
    for target_val in range(16):
        desired_val = (target_val * a_pow) % 18
        if desired_val != target_val:
            ctrl_bits = format(target_val, f"0{N_TARGET}b")
            out_bits = format(desired_val, f"0{N_TARGET}b")
            ops_needed = []
            for i in range(N_TARGET):
                if ctrl_bits[i] != out_bits[i]:
                    ops_needed.append(i)
            if len(ops_needed) == 1:
                qml.ctrl(
                    qml.PauliX(wires=N_PREC + ops_needed[0]),
                    control=list(range(N_PREC)),
                    control_values=[int(b) for b in ctrl_bits],
                )


@qml.qnode(dev)
def shor_circuit(a: int) -> qml.typing.Result:
    """Quantum order-finding circuit for f(x) = a^x mod 15."""
    qml.PauliX(wires=N_PREC)
    qml.Hadamard(wires=range(N_PREC))
    for k in range(N_PREC):
        power = 2**k
        a_pow = pow(a, power, N)
        for i in range(N_TARGET):
            qml.ctrl(qml.Pow(qml.PauliX(wires=N_PREC + i), a_pow),
                     control=k)
    qml.adjoint(qml.QFT(wires=list(range(N_PREC))))
    return qml.probs(wires=range(N_PREC))


def measure_order(a: int) -> int | None:
    """Extract the order r from the QPE measurement."""
    probs = shor_circuit(a)
    measured = np.argmax(probs)
    if measured == 0:
        return None
    phase = measured / (2**N_PREC)
    r = int(round(1 / phase)) if phase > 0 else None
    if r is not None and pow(a, r, N) == 1:
        return r
    return None


def factor(n: int, rng: np.random.Generator) -> tuple[int, int]:
    """Run Shor's algorithm to factor n."""
    while True:
        a = int(rng.integers(2, n))
        g = gcd(a, n)
        if g != 1:
            return g, n // g
        r = measure_order(a)
        if r is not None and r % 2 == 0:
            x = pow(a, r // 2, n)
            if x not in (1, n - 1):
                f1 = gcd(x - 1, n)
                f2 = gcd(x + 1, n)
                if 1 < f1 < n:
                    return f1, n // f1
                if 1 < f2 < n:
                    return f2, n // f2


def main() -> None:
    print(f"=== Shor's Algorithm — Factoring {N} ===")
    print(f"Precision qubits: {N_PREC},  Target qubits: {N_TARGET}")
    print()

    a = 7
    print(f"Order-finding for a = {a}:")
    print(qml.draw(shor_circuit)(a))
    print()

    probs = shor_circuit(a)
    measured = np.argmax(probs)
    phase = measured / (2**N_PREC)
    print(f"  Measured: |{measured:0{N_PREC}b}⟩  phase ≈ {phase:.4f}")
    r = measure_order(a)
    if r is not None:
        print(f"  Recovered order: r = {r}")
        print(f"  Verify: {a}^{r} mod {N} = {pow(a, r, N)}")
    print()

    rng = np.random.default_rng(42)
    p, q = factor(N, rng)
    print(f"Factorization: {N} = {p} × {q}")
    print(f"Verify: {p} × {q} = {p * q}")


if __name__ == "__main__":
    main()
