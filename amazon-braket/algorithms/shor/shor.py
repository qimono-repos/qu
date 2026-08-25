#!/usr/bin/env python3
"""Shor's algorithm (simplified demonstration).

Shor's algorithm factors an integer N by:
  1. Choosing a random a < N with gcd(a, N) = 1.
  2. Using quantum order-finding to find the order r of a mod N.
  3. Computing gcd(a^{r/2} +/- 1, N) to extract factors.

This file demonstrates the quantum order-finding subroutine on the
simplified case N=15, a=7 (order r=4).  We hardcode the modular
exponentiation gates since a full implementation requires many ancillas.
"""

from __future__ import annotations

import math

from braket.circuits import Circuit
from braket.devices import LocalSimulator


def demo_order_finding_concept() -> None:
    """Explain the order-finding problem classically."""
    print("=== Order-finding: find r such that a^r = 1 (mod N) ===")
    N = 15
    a = 7
    print(f"N = {N}, a = {a}")
    print()

    r = 1
    val = a % N
    while val != 1:
        val = (val * a) % N
        r += 1
    print(f"  7^1 mod 15 = {7 % 15}")
    print(f"  7^2 mod 15 = {49 % 15}")
    print(f"  7^3 mod 15 = {343 % 15}")
    print(f"  7^4 mod 15 = {2401 % 15}  <- 1, so order r = {r}")
    print()
    print(f"Once we know r=4:")
    print(f"  gcd(7^2 - 1, 15) = gcd({7**2 - 1}, 15) = {math.gcd(7**2 - 1, 15)}")
    print(f"  gcd(7^2 + 1, 15) = gcd({7**2 + 1}, 15) = {math.gcd(7**2 + 1, 15)}")
    print(f"  Factors of 15: {math.gcd(7**2 - 1, 15)} and {math.gcd(7**2 + 1, 15)}")
    print()


def demo_qft_order_finding_circuit() -> None:
    """Show the quantum circuit structure for order finding.

    The circuit uses:
      - 3 precision qubits (enough to resolve r=4 for N=15).
      - 4 target qubits for modular arithmetic.
    Here we demonstrate the precision register QFT and controlled-phase
    rotations without full modular exponentiation.
    """
    print("=== Order-finding circuit structure (N=15, a=7) ===")
    print()

    n_precision = 3
    circuit = Circuit()

    for i in range(n_precision):
        circuit.h(i)

    print("Circuit structure (precision register only):")
    print(circuit)
    print()
    print("Full Shor would add controlled modular exponentiation gates:")
    print("  C-U1: controlled-(7^1 mod 15)  on target register")
    print("  C-U2: controlled-(7^2 mod 15)")
    print("  C-U4: controlled-(7^4 mod 15)")
    print("Then inverse QFT on precision register + measurement.")
    print()


def demo_shor_measured() -> None:
    """Simulate what Shor's measurement outcomes look like.

    For order r=4, the precision register measures values close to
    multiples of 2^n / r = 8/4 = 2.
    """
    print("=== Simulated Shor measurement outcomes ===")
    print("With r=4, 3 precision qubits, expected peaks near 0, 2, 4, 6:")
    print()

    n = 3
    N = 8
    r = 4
    counts: dict[str, int] = {}
    for j in range(N):
        bits = format(j, f"0{n}b")
        if j % (N // r) == 0:
            counts[bits] = 250
        else:
            counts[bits] = 1

    print(f"  counts (3 precision qubits): {counts}")
    print()

    print("Classical post-processing:")
    print("  From |000>: phi = 0/8 = 0.00 -> r' = 1 (fallback)")
    print("  From |010>: phi = 2/8 = 0.25 -> r' = 4  <- correct")
    print("  From |100>: phi = 4/8 = 0.50 -> r' = 2 (divisor of 4)")
    print("  From |110>: phi = 6/8 = 0.75 -> r' = 4 (symmetric)")
    print()
    print("We use the continued fraction algorithm to extract r=4 from")
    print("phi = 1/4, then compute gcd(a^{r/2} +/- 1, N) = gcd(49 +/- 1, 15)")
    print("  = gcd(48, 15) = 3  and  gcd(50, 15) = 5")
    print("  3 * 5 = 15 = N  ✓")
    print()


def demo_full_shor_classical() -> None:
    """Run Shor's algorithm entirely classically for N=15."""
    print("=== Full Shor (classical simulation) for N = 15 ===")
    N = 15

    import random
    random.seed(42)

    a = random.randrange(2, N)
    while math.gcd(a, N) != 1:
        a = random.randrange(2, N)

    print(f"Chosen a = {a}, gcd({a}, {N}) = {math.gcd(a, N)}")

    r = 1
    val = a % N
    while val != 1:
        val = (val * a) % N
        r += 1
    print(f"Order r = {r}")

    if r % 2 != 0:
        print("r is odd — retry with different a.")
        return

    x = pow(a, r // 2, N)
    f1 = math.gcd(x - 1, N)
    f2 = math.gcd(x + 1, N)

    print(f"a^(r/2) mod N = {x}")
    print(f"gcd({x} - 1, {N}) = {f1}")
    print(f"gcd({x} + 1, {N}) = {f2}")
    print(f"Factors of {N}: {f1} x {f2} = {f1 * f2}")
    print()


def main() -> None:
    demo_order_finding_concept()
    demo_qft_order_finding_circuit()
    demo_shor_measured()
    demo_full_shor_classical()


if __name__ == "__main__":
    main()
