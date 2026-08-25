#!/usr/bin/env python3
"""Phase gates: S, T, and their effects on |+>.

Apply H, S, T gates to show how they rotate phase around the z-axis
without changing measurement probabilities in the computational basis.
"""

from __future__ import annotations

import json

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def demo_hadamard() -> None:
    """H creates equal superposition from |0>."""
    print("=== H|0> = (|0> + |1>)/sqrt(2) ===")
    circuit = Circuit()
    circuit.h(0)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    amps = result.result_types[0].value
    probs = result.result_types[1].value
    print(f"amplitudes: {amps}")
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print()


def demo_s_gate() -> None:
    """S gate adds pi/2 phase to |1> component: S|+> = (|0> + i|1>)/sqrt(2)."""
    print("=== S|+> = (|0> + i|1>)/sqrt(2) ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.s(0)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    amps = result.result_types[0].value
    probs = result.result_types[1].value
    print(f"amplitudes: {amps}")
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print("S adds pi/2 phase to |1>: same probs, different phase")
    print()


def demo_s_dagger() -> None:
    """S-dag reverses the S gate: S+S|+> = |+>."""
    print("=== S+S|+> = |+> (S-dag undoes S) ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.s(0)
    circuit.s(0).dagger()
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    amps = result.result_types[0].value
    print(f"amplitudes: {amps}")
    print()


def demo_t_gate() -> None:
    """T gate adds pi/4 phase to |1> component."""
    print("=== T|+> = (|0> + e^(i*pi/4)|1>)/sqrt(2) ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.t(0)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    amps = result.result_types[0].value
    probs = result.result_types[1].value
    print(f"amplitudes: {amps}")
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print("T adds pi/4 phase to |1>: same probs as |+>, finer phase")
    print()


def demo_t_dagger() -> None:
    """T-dag reverses T: T+T|+> = |+>."""
    print("=== T+T|+> = |+> (T-dag undoes T) ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.t(0)
    circuit.t(0).dagger()
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    amps = result.result_types[0].value
    print(f"amplitudes: {amps}")
    print()


def demo_phase_chain() -> None:
    """Chain S and T: T*S|+> adds 3pi/4 phase to |1>."""
    print("=== T*S|+> = (|0> + e^(i*3pi/4)|1>)/sqrt(2) ===")
    circuit = Circuit()
    circuit.h(0)
    circuit.s(0)
    circuit.t(0)
    print(circuit)
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    probs = result.result_types[1].value
    print(f"probabilities: {json.dumps({k: round(v, 6) for k, v in probs.items()})}")
    print("Phases compose: S adds pi/2, T adds pi/4, total = 3pi/4")
    print()


def demo_phase_still_50_50() -> None:
    """All phase gates leave Z-basis measurement probabilities at 50/50."""
    print("=== Phase gates don't change Z-basis measurement ===")
    circuits = {
        "H|0>":   [("h",)],
        "S|+>":   [("h",), ("s",)],
        "T|+>":   [("h",), ("t",)],
        "T*S|+>": [("h",), ("s",), ("t",)],
    }
    device = LocalSimulator()
    for name, gate_list in circuits.items():
        circuit = Circuit()
        for gates in gate_list:
            for g in gates:
                getattr(circuit, g)(0)
        result = device.run(circuit, shots=2000).result()
        probs = result.result_types[1].value
        print(f"  {name}: {json.dumps({k: round(v, 4) for k, v in probs.items()})}")
    print("All are ~50/50 — phase is invisible to Z-measurement.")
    print()


def main() -> None:
    demo_hadamard()
    demo_s_gate()
    demo_s_dagger()
    demo_t_gate()
    demo_t_dagger()
    demo_phase_chain()
    demo_phase_still_50_50()


if __name__ == "__main__":
    main()
