#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=2)


def count_small_factors(n):
    if n <= 1:
        return 0
    count = 0
    d = 2
    while d * d <= n:
        while n % d == 0:
            count += 1
            n //= d
        d += 1
    if n > 1:
        count += 1
    return count


@qml.qnode(dev, diff_method="parameter-shift")
def energy_circuit(params):
    qml.RY(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.Z(0) @ qml.Z(1))


def prime_energy(n, params):
    scale = count_small_factors(n)
    return energy_circuit(params) * (0.5 + scale)


def objective(params, n):
    return prime_energy(n, params)


def main() -> None:
    rng = np.random.default_rng(42)

    test_values = [2, 3, 5, 7, 11, 4, 6, 8, 9, 15]

    print("VQE-style prime identification")
    print("energy = circuit_expectation × (0.5 + factor_count)")
    print("low energy → few factors → likely prime")
    print()

    results = []
    for n in test_values:
        params = rng.normal(0, 0.5, size=2).astype(float, requires_grad=True)
        opt = qml.AdamOptimizer(stepsize=0.1)
        for _ in range(30):
            params = opt.step(objective, params, n=n)
        e = float(prime_energy(n, params))
        results.append((n, e))

    results.sort(key=lambda t: t[1])
    print(f"{'n':>4s}  {'energy':>8s}  {'prime?':>6s}")
    print("-" * 25)
    for n, e in results:
        is_prime = all(n % d != 0 for d in range(2, int(n**0.5) + 1)) and n >= 2
        print(f"{n:4d}  {e:+8.4f}  {'yes' if is_prime else 'no':>6s}")


if __name__ == "__main__":
    main()
