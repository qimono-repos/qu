#!/usr/bin/env python3
"""Bloch sphere visualization of single-qubit states.

Show the Bloch-sphere representation for |0>, |1>, |+>, |->, and |+i>,
using plot_bloch_multivector.  The script also prints the spherical
coordinates (theta, phi) for each state.

Requires the Guix shell environment for numpy/matplotlib:
    ./run python basic/bloch-sphere/bloch_sphere.py
"""

from __future__ import annotations

import math
import cmath

import qiskit as qk

try:
    import numpy as np
    from qiskit.visualization import plot_bloch_multivector
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def run_statevector(qc: qk.QuantumCircuit) -> qk.quantum_info.Statevector:
    """Return the exact statevector for a circuit."""
    return qk.quantum_info.Statevector.from_instruction(qc)


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
        "|0>":  lambda: qk.QuantumCircuit(1),
        "|1>":  lambda: _x_circuit(),
        "|+>":  lambda: _h_circuit(),
        "|->":  lambda: _hx_circuit(),
        "|+i>": lambda: _hs_circuit(),
    }

    for name, make in states.items():
        qc = make()
        sv = run_statevector(qc)
        amps = sv.to_dict()
        alpha = amps.get("0", 0)
        beta = amps.get("1", 0)
        theta, phi = bloch_angles(alpha, beta)
        print(f"{name:>5}: alpha={alpha}, beta={beta}")
        print(f"       theta={theta:.4f} rad ({math.degrees(theta):.1f} deg), "
              f"phi={phi:.4f} rad ({math.degrees(phi):.1f} deg)")
        if HAS_MPL:
            fig = plot_bloch_multivector(sv, title=name)
            safe = name.replace("|", "").replace(">", "")
            fig.savefig(f"bloch_{safe}.png", dpi=100)
            print(f"       saved bloch_{safe}.png")
        print()


def _x_circuit() -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(1)
    qc.x(0)
    return qc


def _h_circuit() -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    return qc


def _hx_circuit() -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(1)
    qc.x(0)
    qc.h(0)
    return qc


def _hs_circuit() -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    qc.s(0)
    return qc


def main() -> None:
    print("=== Bloch sphere: canonical single-qubit states ===\n")
    demo_states()


if __name__ == "__main__":
    main()
