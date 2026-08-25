import cudaq
import numpy as np
from math import gcd


def classical_shor(N: int) -> int:
    """Classical part of Shor's algorithm.
    
    Finds a non-trivial factor of N using the quantum
    order-finding subroutine.
    """
    if N % 2 == 0:
        return 2

    a = 2
    while gcd(a, N) != 1:
        a += 1
    return a


@cudaq.kernel
def order_finding_a2():
    """Quantum circuit for finding the order of a=2 mod N=15.
    
    4 count qubits + 4 work qubits.
    Applies controlled multiplication by 2 mod 15.
    """
    qubits = cudaq.qvector(8)
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    h(qubits[3])
    x(qubits[4])
    cx(qubits[0], qubits[5])
    cx(qubits[0], qubits[6])
    cx(qubits[1], qubits[6])
    cx(qubits[1], qubits[7])
    cx(qubits[2], qubits[5])
    cx(qubits[2], qubits[6])
    cx(qubits[2], qubits[7])
    cx(qubits[3], qubits[5])
    cx(qubits[3], qubits[7])
    swap(qubits[0], qubits[3])
    swap(qubits[1], qubits[2])
    h(qubits[0])
    crz(qubits[0], qubits[1], -np.pi / 2)
    h(qubits[1])
    crz(qubits[0], qubits[2], -np.pi / 4)
    crz(qubits[1], qubits[2], -np.pi / 2)
    h(qubits[2])
    crz(qubits[0], qubits[3], -np.pi / 8)
    crz(qubits[1], qubits[3], -np.pi / 4)
    crz(qubits[2], qubits[3], -np.pi / 2)
    h(qubits[3])


@cudaq.kernel
def order_finding_a7():
    """Quantum circuit for finding the order of a=7 mod N=15."""
    qubits = cudaq.qvector(8)
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    h(qubits[3])
    x(qubits[4])
    cx(qubits[0], qubits[5])
    cx(qubits[0], qubits[6])
    cx(qubits[0], qubits[7])
    cx(qubits[1], qubits[5])
    cx(qubits[1], qubits[6])
    cx(qubits[1], qubits[7])
    cx(qubits[2], qubits[5])
    cx(qubits[2], qubits[7])
    cx(qubits[3], qubits[5])
    cx(qubits[3], qubits[6])
    swap(qubits[0], qubits[3])
    swap(qubits[1], qubits[2])
    h(qubits[0])
    crz(qubits[0], qubits[1], -np.pi / 2)
    h(qubits[1])
    crz(qubits[0], qubits[2], -np.pi / 4)
    crz(qubits[1], qubits[2], -np.pi / 2)
    h(qubits[2])
    crz(qubits[0], qubits[3], -np.pi / 8)
    crz(qubits[1], qubits[3], -np.pi / 4)
    crz(qubits[2], qubits[3], -np.pi / 2)
    h(qubits[3])


def extract_period(counts: dict, n_count: int) -> int:
    """Extract the period from measurement results of the count register."""
    max_count = max(counts.values())
    most_common = [k for k, v in counts.items() if v == max_count][0]
    count_bits = most_common[:n_count]
    s = int(count_bits, 2)
    return s


def continued_fraction(s: int, denom: int) -> int:
    """Find the denominator r from s/2^n using continued fractions."""
    n = 16
    if s == 0:
        return denom
    frac = s / (2 ** n)
    for r in range(1, denom + 1):
        if abs(frac - round(frac * r) / r) < 0.01:
            return r
    return denom


if __name__ == "__main__":
    print("=== Shor's Algorithm (Simplified) ===\n")
    N = 15
    print(f"Factoring N = {N}\n")

    a = classical_shor(N)
    print(f"Step 1: Classical preprocessing")
    print(f"  Chose a = {a} (gcd({a}, {N}) = {gcd(a, N)})")

    print(f"\nStep 2: Quantum order finding")
    if a == 2:
        result = cudaq.sample(order_finding_a2, shots_count=1000)
    else:
        result = cudaq.sample(order_finding_a7, shots_count=1000)

    n_count = 4
    counts = {k: v for k, v in result.items()}
    print(f"  Count register measurements (top 5):")
    sorted_counts = sorted(counts.items(), key=lambda x: -x[1])[:5]
    for bitstring, count in sorted_counts:
        count_bits = bitstring[:n_count]
        s = int(count_bits, 2)
        print(f"    |{bitstring}>: {count}  "
              f"(count = {count_bits} = {s})")

    s = extract_period(counts, n_count)
    print(f"\n  Most likely s = {s}")
    print(f"  s/2^4 = {s}/{2**n_count} = {s/2**n_count:.4f}")

    r = continued_fraction(s, N)
    print(f"\nStep 3: Continued fraction => period r = {r}")

    if r % 2 == 0:
        print(f"\nStep 4: r is even, computing factors")
        x1 = pow(a, r // 2, N)
        x2 = x1 + N
        print(f"  a^(r/2) mod N = {a}^{r//2} mod {N} = {x1}")
        f1 = gcd(x1 - 1, N)
        f2 = gcd(x1 + 1, N)
        print(f"  gcd(a^(r/2) - 1, N) = gcd({x1 - 1}, {N}) = {f1}")
        print(f"  gcd(a^(r/2) + 1, N) = gcd({x1 + 1}, {N}) = {f2}")
        if f1 != 1 and f1 != N:
            print(f"\n  Found non-trivial factor: {N} = {f1} * {N // f1}")
        elif f2 != 1 and f2 != N:
            print(f"\n  Found non-trivial factor: {N} = {f2} * {N // f2}")
    else:
        print(f"\n  r is odd, retry with a different a")

    print("\n--- Quantum Part Summary ---")
    print("1. Create superposition over all exponents")
    print("2. Compute a^x mod N in superposition (oracle)")
    print("3. Apply inverse QFT to extract the period")
    print("4. Measure and use continued fractions")
    print("5. Classically compute gcd(a^(r/2) ± 1, N)")
