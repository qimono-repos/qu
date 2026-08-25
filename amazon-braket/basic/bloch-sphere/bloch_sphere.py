#!/usr/bin/env python3
"""Bloch sphere visualization of single-qubit states.

Show the Bloch-sphere representation for |0>, |1>, |+>, |->, and |+i>,
using the BlochSphereResult from the local simulator. The script also
prints the spherical coordinates (theta, phi) for each state.
"""

from __future__ import annotations

import math
import cmath

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def bloch_angles(alpha: complex, beta: complex) -> tuple[float, float]:
    """Return (theta, phi) for psi = alpha|0> + beta|1>."""
    theta = 2.0 * math.acos(min(1.0, abs(alpha)))
    if abs(beta) > 1e-12:
        phi = cmath.phase(beta)
    else:
        phi = 0.0
    return theta, phi


def demo_states() -> None:
    """Print and visualize several canonical single-qubit states."""
    states = {
        "|0>":  lambda: Circuit(),
        "|1>":  lambda: _x_circuit(),
        "|+>":  lambda: _h_circuit(),
        "|->":  lambda: _hx_circuit(),
        "|+i>": lambda: _hs_circuit(),
    }

    device = LocalSimulator()
    for name, make in states.items():
        circuit = make()
        result = device.run(circuit, shots=0).result()
        amps = result.result_types[0].value
        # amps is a numpy array; index 0 = |0>, index 1 = |1>
        alpha = amps[0]
        beta = amps[1]
        theta, phi = bloch_angles(alpha, beta)
        print(f"{name:>5}: alpha={alpha}, beta={beta}")
        print(f"       theta={theta:.4f} rad ({math.degrees(theta):.1f} deg), "
              f"phi={phi:.4f} rad ({math.degrees(phi):.1f} deg)")
        print()


def _x_circuit() -> Circuit:
    circuit = Circuit()
    circuit.x(0)
    return circuit


def _h_circuit() -> Circuit:
    circuit = Circuit()
    circuit.h(0)
    return circuit


def _hx_circuit() -> Circuit:
    circuit = Circuit()
    circuit.x(0)
    circuit.h(0)
    return circuit


def _hs_circuit() -> Circuit:
    circuit = Circuit()
    circuit.h(0)
    circuit.s(0)
    return circuit


def main() -> None:
    print("=== Bloch sphere: canonical single-qubit states ===")
    print()
    demo_states()


if __name__ == "__main__":
    main()
