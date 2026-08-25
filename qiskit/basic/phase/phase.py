#!/usr/bin/env python3
"""Phase gates: S, T, and their effects on |+>.

Apply H, S, T gates to show how they rotate phase around the z-axis
without changing measurement probabilities in the computational basis.
"""

from __future__ import annotations

import qiskit as qk
import qiskit_aer as qka


def run_statevector(qc: qk.QuantumCircuit) -> qk.quantum_info.Statevector:
    """Return the exact statevector for a circuit."""
    return qk.quantum_info.Statevector.from_instruction(qc)


def run_shots(qc: qk.QuantumCircuit, shots: int = 1024) -> dict[str, int]:
    """Execute a circuit with measurement on Aer and return counts."""
    measured = qc.copy()
    if measured.num_clbits == 0:
        measured.measure_all()
    backend = qka.AerSimulator()
    compiled = qk.transpile(measured, backend)
    return backend.run(compiled, shots=shots).result().get_counts()


def demo_hadamard() -> None:
    """H creates equal superposition from |0>."""
    print("=== H|0> = (|0> + |1>)/sqrt(2) ===")
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        print(f"  {a:.4f} |{b}>")
    print("probs:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print()


def demo_s_gate() -> None:
    """S gate adds pi/2 phase to |1> component: S|+> = (|0> + i|1>)/sqrt(2)."""
    print("=== S|+> = (|0> + i|1>)/sqrt(2) ===")
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    qc.s(0)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        print(f"  {a:.4f} |{b}>")
    print("probs:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print("S adds pi/2 phase to |1>: same probs, different phase\n")


def demo_s_dagger() -> None:
    """S-dag reverses the S gate: S+S|+> = |+>."""
    print("=== S+S|+> = |+> (S-dag undoes S) ===")
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    qc.s(0)
    qc.sdg(0)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        print(f"  {a:.4f} |{b}>")
    print()


def demo_t_gate() -> None:
    """T gate adds pi/4 phase to |1> component."""
    print("=== T|+> = (|0> + e^(i*pi/4)|1>)/sqrt(2) ===")
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    qc.t(0)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        print(f"  {a:.4f} |{b}>")
    print("probs:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print("T adds pi/4 phase to |1>: same probs as |+>, finer phase\n")


def demo_t_dagger() -> None:
    """T-dag reverses T: T+T|+> = |+>."""
    print("=== T+T|+> = |+> (T-dag undoes T) ===")
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    qc.t(0)
    qc.tdg(0)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        print(f"  {a:.4f} |{b}>")
    print()


def demo_phase_chain() -> None:
    """Chain S and T: T*S|+> adds 3pi/4 phase to |1>."""
    print("=== T*S|+> = (|0> + e^(i*3pi/4)|1>)/sqrt(2) ===")
    qc = qk.QuantumCircuit(1)
    qc.h(0)
    qc.s(0)
    qc.t(0)
    print(qc.draw(output="text"))
    sv = run_statevector(qc)
    for b, a in sv.to_dict().items():
        print(f"  {a:.4f} |{b}>")
    print("probs:", {k: round(v, 4) for k, v in sv.probabilities_dict().items()})
    print("Phases compose: S adds pi/2, T adds pi/4, total = 3pi/4\n")


def _make_circ(*gates: str) -> qk.QuantumCircuit:
    """Build a 1-qubit circuit with the named gates in order."""
    qc = qk.QuantumCircuit(1)
    for g in gates:
        getattr(qc, g)(0)
    return qc


def demo_phase_still_50_50() -> None:
    """All phase gates leave Z-basis measurement probabilities at 50/50."""
    print("=== Phase gates don't change Z-basis measurement ===")
    circuits = {
        "H|0>":   _make_circ("h"),
        "S|+>":   _make_circ("h", "s"),
        "T|+>":   _make_circ("h", "t"),
        "T*S|+>": _make_circ("h", "s", "t"),
    }
    for name, qc in circuits.items():
        counts = run_shots(qc, shots=2000)
        print(f"  {name}: {counts}")
    print("All are ~50/50 — phase is invisible to Z-measurement.\n")


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
