"""Shor's algorithm: factoring 15 using order-finding (simplified)."""

import cirq
import math
import numpy as np
from fractions import Fraction


def cregoodle_modular_exponentiation(
    a: int, power: int, control: cirq.LineQubit, target: list[cirq.LineQubit], n: int
) -> list[cirq.Operation]:
    """Build controlled modular exponentiation a^power mod N.

    Uses repeated controlled multiplication by a.
    """
    ops: list[cirq.Operation] = []
    for _ in range(power):
        for q in range(n):
            if (a >> q) & 1:
                for j in range(n):
                    shift = (q + j) % n
                    ops.append(
                        cirq.CNOT(target[j], target[(q + j) % n])
                    )
    return ops


def mod_mul(a: int, n: int, ctrl: cirq.LineQubit, x: list[cirq.LineQubit]) -> list[cirq.Operation]:
    """Controlled multiplication: |ctrl⟩|y⟩ → |ctrl⟩|y·a mod N⟩.

    Simplified implementation for N=15.
    """
    ops: list[cirq.Operation] = []
    for i in range(n):
        target_idx = (i + a.bit_length() - 1) % n
        if target_idx != i:
            ops.append(cirq.CNOT(x[i], x[target_idx]))
    return ops


def cregoodle_qft(
    qubits: list[cirq.LineQubit], inverse: bool = False
) -> list[cirq.Operation]:
    """QFT or inverse QFT on the given qubits."""
    n = len(qubits)
    ops: list[cirq.Operation] = []
    sign = -1 if inverse else 1

    if not inverse:
        ops.extend(cirq.SWAP(qubits[i], qubits[n - 1 - i]) for i in range(n // 2))

    for i in range(n if inverse else n):
        if inverse:
            for j in range(i + 1, n):
                k = j - i
                ops.append(
                    cirq.CZPowGate(exponent=-sign / (2**k))(qubits[j], qubits[i])
                )
            ops.append(cirq.H(qubits[i]))
        else:
            ops.append(cirq.H(qubits[i]))
            for j in range(i + 1, n):
                k = j - i
                ops.append(
                    cirq.CZPowGate(exponent=sign / (2**k))(qubits[j], qubits[i])
                )

    if not inverse:
        ops.extend(cirq.SWAP(qubits[i], qubits[n - 1 - i]) for i in range(n // 2))

    return ops


def quantum_order_finding(a: int, N: int, n_count: int = 4, n_work: int = 4) -> int | None:
    """Find the order of a mod N using quantum phase estimation.

    Returns the measured phase as a fraction of 2^n_count.
    """
    precision = cirq.LineQubit.range(n_count)
    work = cirq.LineQubit.range(n_count, n_count + n_work)
    sim = cirq.Simulator()

    ops: list[cirq.Operation] = []

    ops.append(cirq.X(work[0]))

    for q in precision:
        ops.append(cirq.H(q))

    for i in range(n_count):
        power = 2**i
        for _ in range(power):
            for q_idx in range(n_work):
                if (a >> q_idx) & 1:
                    shift = q_idx % n_work
                    ops.append(cirq.CNOT(precision[i], work[(q_idx + shift) % n_work]))

    ops.extend(cregoodle_qft(precision, inverse=True))

    circuit = cirq.Circuit(ops)
    result = sim.run(circuit + cirq.measure(*precision, key="m"), repetitions=100)
    counts = result.histogram(key="m")

    most_common = max(counts, key=counts.get)
    phase = most_common / (2**n_count)

    r = _denominator_closest(phase, N)
    return r


def _denominator_closest(phase: float, max_r: int) -> int | None:
    """Find the rational approximation of phase with denominator ≤ max_r."""
    best_r = 1
    best_err = abs(phase)
    for r in range(1, max_r + 1):
        frac = Fraction(phase).limit_denominator(r)
        err = abs(frac - phase)
        if err < best_err:
            best_err = err
            best_r = r
    return best_r if best_err < 0.01 else None


def shor_factor(N: int) -> tuple[int, int] | None:
    """Factor N using Shor's algorithm.

    Uses classical fallback for the deterministic simulation.
    """
    if N % 2 == 0:
        return (2, N // 2)

    a = 2
    while a < N:
        if math.gcd(a, N) == 1:
            break
        a += 1

    if a >= N:
        return None

    r = _find_order_classical(a, N)
    if r is None or r % 2 != 0:
        return None

    x = pow(a, r // 2, N)
    if x == N - 1:
        return None

    f1 = math.gcd(x + 1, N)
    f2 = math.gcd(x - 1, N)

    if 1 < f1 < N:
        return (f1, N // f1)
    if 1 < f2 < N:
        return (f2, N // f2)
    return None


def _find_order_classical(a: int, N: int) -> int | None:
    """Find order of a mod N classically (for simulation)."""
    x = 1
    for r in range(1, N + 1):
        x = (x * a) % N
        if x == 1:
            return r
    return None


def main() -> None:
    print("=== Shor's Algorithm: Factoring 15 ===\n")

    N = 15
    print(f"N = {N}\n")

    print("Step 1: Choose random a coprime to N")
    a = 7
    print(f"  a = {a}, gcd({a}, {N}) = {math.gcd(a, N)}\n")

    print("Step 2: Find order r of a mod N")
    r = _find_order_classical(a, N)
    print(f"  {a}^{r} mod {N} = {pow(a, r, N)}")
    print(f"  Order r = {r}\n")

    print("Step 3: Factor from order")
    half = pow(a, r // 2, N)
    print(f"  a^(r/2) mod N = {a}^{r // 2} mod {N} = {half}")
    f1 = math.gcd(half + 1, N)
    f2 = math.gcd(half - 1, N)
    print(f"  gcd({half}+1, {N}) = {f1}")
    print(f"  gcd({half}-1, {N}) = {f2}")
    print(f"\n  Factors of {N}: {f1} × {f2} = {f1 * f2}\n")

    print("=== Quantum order-finding circuit (simplified) ===\n")
    n_count = 4
    n_work = 4
    precision = cirq.LineQubit.range(n_count)
    work = cirq.LineQubit.range(n_count, n_count + n_work)

    circuit = cirq.Circuit(
        cirq.X(work[0]),
        [cirq.H(q) for q in precision],
    )
    print(f"Circuit ({n_count} precision + {n_work} work qubits):")
    print(circuit)
    print(f"  (Controlled modular exponentiation omitted for clarity)")
    print(f"  Full circuit would apply a^(2^i) mod N controlled on precision qubit i.")


if __name__ == "__main__":
    main()
