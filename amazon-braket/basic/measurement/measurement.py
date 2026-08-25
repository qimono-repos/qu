#!/usr/bin/env python3
"""Measurement in Z and X bases.

Demonstrate how the same state gives different measurement statistics
depending on the measurement basis.  Measure in the Z basis (default)
and the X basis (H before measurement).
"""

from __future__ import annotations

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def z_basis_measure(state_prep: Circuit, shots: int = 1000) -> dict[str, int]:
    """Measure qubit in the Z basis (computational basis)."""
    measured = Circuit()
    measured.add_circuit(state_prep)
    measured.measure(0)
    device = LocalSimulator()
    result = device.run(measured, shots=shots).result()
    return result.result_types[0].value


def x_basis_measure(state_prep: Circuit, shots: int = 1000) -> dict[str, int]:
    """Measure qubit in the X basis (H before measurement)."""
    measured = Circuit()
    measured.add_circuit(state_prep)
    measured.h(0)
    measured.measure(0)
    device = LocalSimulator()
    result = device.run(measured, shots=shots).result()
    return result.result_types[0].value


def print_counts(name: str, counts: dict[str, int], shots: int) -> None:
    """Pretty-print measurement counts with fractions."""
    print(f"  {name}:")
    for state in sorted(counts, key=counts.get, reverse=True):  # type: ignore[arg-type]
        frac = counts[state] / shots
        print(f"    |{state}>: {counts[state]:>4}/{shots}  ({frac:.1%})")
    print()


def demo_z0_state() -> None:
    """|0> measured in Z and X bases."""
    print("=== |0> state ===")
    prep = Circuit()
    device = LocalSimulator()
    result = device.run(prep, shots=0).result()
    print(f"  amplitudes: {result.result_types[0].value}")

    z_counts = z_basis_measure(prep)
    print_counts("Z-basis", z_counts, 1000)

    x_counts = x_basis_measure(prep)
    print_counts("X-basis", x_counts, 1000)


def demo_x_state() -> None:
    """|+> = H|0> measured in Z and X bases."""
    print("=== |+> = H|0> state ===")
    prep = Circuit()
    prep.h(0)
    device = LocalSimulator()
    result = device.run(prep, shots=0).result()
    print(f"  amplitudes: {result.result_types[0].value}")

    z_counts = z_basis_measure(prep)
    print_counts("Z-basis (random 50/50)", z_counts, 1000)

    x_counts = x_basis_measure(prep)
    print_counts("X-basis (deterministic |+>)", x_counts, 1000)


def demo_minus_state() -> None:
    """|-> = HX|0> measured in Z and X bases."""
    print("=== |-> = HX|0> state ===")
    prep = Circuit()
    prep.x(0)
    prep.h(0)
    device = LocalSimulator()
    result = device.run(prep, shots=0).result()
    print(f"  amplitudes: {result.result_types[0].value}")

    z_counts = z_basis_measure(prep)
    print_counts("Z-basis (random 50/50)", z_counts, 1000)

    x_counts = x_basis_measure(prep)
    print_counts("X-basis (deterministic |->)", x_counts, 1000)


def demo_one_state() -> None:
    """|1> measured in Z and X bases."""
    print("=== |1> state ===")
    prep = Circuit()
    prep.x(0)
    device = LocalSimulator()
    result = device.run(prep, shots=0).result()
    print(f"  amplitudes: {result.result_types[0].value}")

    z_counts = z_basis_measure(prep)
    print_counts("Z-basis", z_counts, 1000)

    x_counts = x_basis_measure(prep)
    print_counts("X-basis (random 50/50)", x_counts, 1000)


def main() -> None:
    demo_z0_state()
    demo_x_state()
    demo_minus_state()
    demo_one_state()


if __name__ == "__main__":
    main()
