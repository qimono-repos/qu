#!/usr/bin/env python3
"""Grover's search algorithm on 3 qubits (N=8).

Grover's algorithm finds a marked item in an unsorted list of N items
using only O(sqrt(N)) oracle queries.  On 3 qubits we search N=8
states and mark |101> (5).  One Grover iteration gives a ~95%
probability of measuring the target.
"""

from __future__ import annotations

from braket.circuits import Circuit, ResultType
from braket.devices import LocalSimulator


def sv_probs(circuit: Circuit) -> tuple[list[complex], list[float]]:
    """Run circuit with statevector + probability result types."""
    circuit.add_result_type(ResultType.StateVector())
    circuit.add_result_type(ResultType.Probability())
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    sv = [complex(a) for a in result.result_types[0].value]
    probs = [float(p) for p in result.result_types[1].value]
    return sv, probs


def oracle_mark_101() -> Circuit:
    """Oracle that flips the phase of |101>.

    Map |101> -> |111> with X(1), apply CCZ via H-CCX-H, then undo.
    """
    circuit = Circuit()
    circuit.x(1)
    circuit.h(2)
    circuit.ccnot(0, 1, 2)
    circuit.h(2)
    circuit.x(1)
    return circuit


def diffusion_operator(n: int = 3) -> Circuit:
    """Grover diffusion operator: 2|s><s| - I where |s> = H^n|0>^n.

    Equivalent to: H^n (2|0><0| - I) H^n.
    The 2|0><0| - I operator flips the phase of all states except |0>.
    Implemented as: X^n, then multi-controlled Z via H-CCX-H on last qubit.
    """
    circuit = Circuit()
    for i in range(n):
        circuit.h(i)
    for i in range(n):
        circuit.x(i)
    circuit.h(n - 1)
    circuit.ccnot(0, 1, 2)
    circuit.h(n - 1)
    for i in range(n):
        circuit.x(i)
    for i in range(n):
        circuit.h(i)
    return circuit


def grover_circuit(iterations: int = 1, target: int = 5, n: int = 3) -> Circuit:
    """Build the Grover search circuit.

    For N=8, the optimal number of iterations is 1 (pi/4 * sqrt(8) ~ 2.2).
    """
    circuit = Circuit()
    for i in range(n):
        circuit.h(i)

    for _ in range(iterations):
        circuit.add_circuit(oracle_mark_101())
        circuit.add_circuit(diffusion_operator(n))

    for i in range(n):
        circuit.measure(i)
    return circuit


def demo_grover_1iter() -> None:
    """Single Grover iteration searching for |101>."""
    print("=== Grover search for |101> (1 iteration, N=8) ===")
    circuit = grover_circuit(iterations=1, target=5)
    print(circuit)

    device = LocalSimulator()
    result = device.run(circuit, shots=1000).result()
    counts = dict(result.measurement_counts)

    print(f"counts: {counts}")
    target_prob = counts.get("101", 0) / 1000
    print(f"P(|101>) = {target_prob:.1%}  (expected ~94.5%)")
    print()


def demo_grover_2iter() -> None:
    """Two Grover iterations — over-rotation shows decreasing probability."""
    print("=== Grover search for |101> (2 iterations) ===")
    circuit = grover_circuit(iterations=2, target=5)

    device = LocalSimulator()
    result = device.run(circuit, shots=1000).result()
    counts = dict(result.measurement_counts)

    print(f"counts: {counts}")
    target_prob = counts.get("101", 0) / 1000
    print(f"P(|101>) = {target_prob:.1%}  (over-rotated, probability decreased)")
    print()


def demo_amplitude_inspection() -> None:
    """Show amplitudes after each Grover iteration."""
    print("=== Amplitude evolution during Grover search ===")

    n = 3
    circuit = Circuit()
    for i in range(n):
        circuit.h(i)
    sv, probs = sv_probs(circuit)
    print("After H^n (uniform superposition):")
    for k in range(8):
        bits = format(k, "03b")
        print(f"  |{bits}>  amp = {sv[k]:+.4f}  |amp|^2 = {abs(sv[k])**2:.4f}")
    print()

    circuit2 = Circuit()
    for i in range(n):
        circuit2.h(i)
    circuit2.add_circuit(oracle_mark_101())
    sv2, _ = sv_probs(circuit2)
    print("After oracle (|101> phase flipped):")
    for k in range(8):
        bits = format(k, "03b")
        print(f"  |{bits}>  amp = {sv2[k]:+.4f}  |amp|^2 = {abs(sv2[k])**2:.4f}")
    print()

    circuit3 = Circuit()
    for i in range(n):
        circuit3.h(i)
    circuit3.add_circuit(oracle_mark_101())
    circuit3.add_circuit(diffusion_operator(n))
    sv3, _ = sv_probs(circuit3)
    print("After diffusion (amplitude amplified):")
    for k in range(8):
        bits = format(k, "03b")
        marker = " <-- target" if k == 5 else ""
        print(f"  |{bits}>  amp = {sv3[k]:+.4f}  |amp|^2 = {abs(sv3[k])**2:.4f}{marker}")
    print()


def main() -> None:
    demo_grover_1iter()
    demo_grover_2iter()
    demo_amplitude_inspection()


if __name__ == "__main__":
    main()
