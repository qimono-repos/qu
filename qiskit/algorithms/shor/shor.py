#!/usr/bin/env python3
"""Shor's algorithm: factor N = 15 by quantum period finding.

This is a from-scratch, self-contained walkthrough. The modular
multiplier a^x mod 15 is a small hand-built circuit (not taken from
qiskit-algorithms), the inverse QFT is written gate-by-gate, and the
classical post-processing (continued fractions + gcd) lives here too.
"""

from __future__ import annotations

import qiskit as qk
import qiskit_aer as qka


class std:
    import math
    import fractions


N = 15
A = 7
COUNTING_QUBITS = 8


def coprime_ok(a: int, n: int) -> None:
    if std.math.gcd(a, n) != 1:
        raise ValueError(f"{a} shares a factor with {n}; pick another base")


def multiply_amod15(a: int) -> qk.QuantumCircuit:
    """Unitary that sends |k> to |a*k mod 15> on four qubits.

    Only the bases coprime to 15 that the usual textbook circuit covers
    are accepted. Each case is a handful of SWAPs and X gates.
    """
    if a not in (2, 4, 7, 8, 11, 13):
        raise ValueError("this demo circuit only knows a in {2,4,7,8,11,13}")
    u = qk.QuantumCircuit(4, name=f"*{a} mod 15")
    if a in (2, 13):
        u.swap(2, 3)
        u.swap(1, 2)
        u.swap(0, 1)
    if a in (7, 8):
        u.swap(0, 1)
        u.swap(1, 2)
        u.swap(2, 3)
    if a in (4, 11):
        u.swap(1, 3)
        u.swap(0, 2)
    if a in (7, 11, 13):
        for q in range(4):
            u.x(q)
    return u


def controlled_power(a: int, exponent: int) -> qk.QuantumCircuit:
    """Controlled multiplication by a^{exponent} mod 15."""
    body = qk.QuantumCircuit(4, name=f"{a}^{exponent} mod 15")
    for _ in range(exponent):
        body.compose(multiply_amod15(a), inplace=True)
    gate = body.to_gate()
    gate.name = f"{a}^{exponent} mod 15"
    return gate.control(1)


def inverse_qft(n: int) -> qk.QuantumCircuit:
    """Hand-rolled inverse QFT on n qubits (swap-endian, then inverse phases)."""
    iqft = qk.QuantumCircuit(n, name="IQFT")
    for i in range(n // 2):
        iqft.swap(i, n - 1 - i)
    for j in range(n):
        for k in range(j):
            iqft.cp(-std.math.pi / 2 ** (j - k), k, j)
        iqft.h(j)
    return iqft


def period_finding_circuit(a: int, counting_qubits: int) -> qk.QuantumCircuit:
    counting = qk.QuantumRegister(counting_qubits, "phase")
    work = qk.QuantumRegister(4, "work")
    bits = qk.ClassicalRegister(counting_qubits, "m")
    qc = qk.QuantumCircuit(counting, work, bits, name="shor15")

    qc.h(counting)
    qc.x(work[0])  # work register starts at |1>

    for k, qubit in enumerate(counting):
        qc.append(controlled_power(a, 2**k), [qubit, *work])

    qc.append(inverse_qft(counting_qubits), counting)
    qc.measure(counting, bits)
    return qc


def continued_fraction_period(measured: int, counting_qubits: int, n: int) -> int | None:
    """Estimate the period r from a single phase bitstring."""
    if measured == 0:
        return None
    phase = measured / (2**counting_qubits)
    approx = std.fractions.Fraction(phase).limit_denominator(n)
    r = approx.denominator
    if r == 0 or r > n:
        return None
    return r


def factors_from_period(a: int, r: int, n: int) -> tuple[int, int] | None:
    if r % 2 == 1:
        return None
    x = pow(a, r // 2, n)
    if x in (1, n - 1):
        return None
    p = std.math.gcd(x - 1, n)
    q = std.math.gcd(x + 1, n)
    if p * q == n and 1 < p < n and 1 < q < n:
        return (p, q)
    if 1 < p < n:
        return (p, n // p)
    if 1 < q < n:
        return (q, n // q)
    return None


def most_common_nonzero(counts: dict[str, int]) -> list[tuple[int, int]]:
    ranked = []
    for bitstring, shots in counts.items():
        value = int(bitstring.replace(" ", ""), 2)
        if value != 0:
            ranked.append((value, shots))
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked


def main() -> None:
    coprime_ok(A, N)
    print(f"Shor period finding for N={N}, base a={A}")
    print(f"classical check: {[pow(A, x, N) for x in range(1, 9)]}")
    print("period of 7^x mod 15 is 4 (7, 4, 13, 1, ...)\n")

    qc = period_finding_circuit(A, COUNTING_QUBITS)
    print(qc.draw(output="text", fold=-1))

    backend = qka.AerSimulator()
    counts = backend.run(qk.transpile(qc, backend), shots=128).result().get_counts()
    print("\nmeasured phases (top 8):")
    for bitstring, shots in sorted(counts.items(), key=lambda kv: -kv[1])[:8]:
        value = int(bitstring, 2)
        print(f"  {bitstring}  = {value:3d}/2^{COUNTING_QUBITS}  ({value / 2**COUNTING_QUBITS:.4f})  x{shots}")

    print("\ncontinued-fraction candidates:")
    seen: set[int] = set()
    found: tuple[int, int] | None = None
    for value, _shots in most_common_nonzero(counts):
        r = continued_fraction_period(value, COUNTING_QUBITS, N)
        if r is None or r in seen:
            continue
        seen.add(r)
        pair = factors_from_period(A, r, N)
        mark = ""
        if pair is not None:
            found = pair
            mark = f"  -> factors {pair}"
        print(f"  phase {value}/{2**COUNTING_QUBITS}  r={r}{mark}")
        if found is not None:
            break

    if found is None:
        print("no even period that splits 15 showed up; re-run (shot noise)")
    else:
        p, q = found
        print(f"\n{N} = {p} x {q}")


if __name__ == "__main__":
    main()
