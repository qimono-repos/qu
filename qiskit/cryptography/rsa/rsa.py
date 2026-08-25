#!/usr/bin/env python3
"""Integer factorization via Shor's algorithm — the quantum threat to RSA.

This is NOT an RSA encryption demo. It factors N=15 using quantum
period-finding to show why large semiprimes are vulnerable.
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


def multiply_amod15(a: int) -> qk.QuantumCircuit:
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


def controlled_power(a: int, exponent: int) -> qk.Gate:
    body = qk.QuantumCircuit(4, name=f"{a}^{exponent} mod 15")
    for _ in range(exponent):
        body.compose(multiply_amod15(a), inplace=True)
    gate = body.to_gate()
    gate.name = f"{a}^{exponent} mod 15"
    return gate.control(1)


def inverse_qft(n: int) -> qk.QuantumCircuit:
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
    qc.x(work[0])

    for k, qubit in enumerate(counting):
        qc.append(controlled_power(a, 2**k), [qubit, *work])

    qc.append(inverse_qft(counting_qubits), counting)
    qc.measure(counting, bits)
    return qc


def continued_fraction_period(measured: int, counting_qubits: int, n: int) -> int | None:
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


def main() -> None:
    print(f"RSA threat demo: factor N={N} via quantum period-finding")
    print(f"base a={A}, classical orbit: {[pow(A, x, N) for x in range(1, 9)]}")
    print(f"period of {A}^x mod {N} is 4\n")

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
    for bitstring, _shots in sorted(counts.items(), key=lambda kv: -kv[1]):
        value = int(bitstring, 2)
        if value == 0:
            continue
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
        print("This is why RSA-2048 needs 2048-bit keys — quantum computers")
        print("could factor them in polynomial time via Shor's algorithm.")


if __name__ == "__main__":
    main()
