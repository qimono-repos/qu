#!/usr/bin/env python3
"""Deutsch–Jozsa on n=2: tell constant from balanced in one query.

A promise function f:{0,1}^n → {0,1} is either constant (same bit on
every input) or balanced (half the inputs map to 0, half to 1).
Classically you may need 2^{n-1}+1 evaluations. The quantum circuit
uses one oracle call.

Four hand-built oracles live in this file. Nothing is imported from
the other algorithm folders.
"""

from __future__ import annotations

from collections.abc import Callable

import qiskit as qk
from qiskit_aer import AerSimulator


N_BITS = 2
ANCILLA = N_BITS  # last qubit of the register of size N_BITS + 1


def oracle_constant_0() -> qk.QuantumCircuit:
    """f(x) = 0. Identity on |x>|y>."""
    return qk.QuantumCircuit(N_BITS + 1, name="f=0")


def oracle_constant_1() -> qk.QuantumCircuit:
    """f(x) = 1. Flip the ancilla for every x."""
    qc = qk.QuantumCircuit(N_BITS + 1, name="f=1")
    qc.x(ANCILLA)
    return qc


def oracle_lsb() -> qk.QuantumCircuit:
    """Balanced: f(x) = x_0 (Qiskit qubit 0, rightmost bit)."""
    qc = qk.QuantumCircuit(N_BITS + 1, name="f=x0")
    qc.cx(0, ANCILLA)
    return qc


def oracle_parity() -> qk.QuantumCircuit:
    """Balanced: f(x) = x_0 XOR x_1."""
    qc = qk.QuantumCircuit(N_BITS + 1, name="f=x0⊕x1")
    qc.cx(0, ANCILLA)
    qc.cx(1, ANCILLA)
    return qc


ORACLES: dict[str, tuple[str, Callable[[], qk.QuantumCircuit]]] = {
    "constant-0": ("constant", oracle_constant_0),
    "constant-1": ("constant", oracle_constant_1),
    "balanced-lsb": ("balanced", oracle_lsb),
    "balanced-parity": ("balanced", oracle_parity),
}


def deutsch_jozsa_circuit(oracle: qk.QuantumCircuit) -> qk.QuantumCircuit:
    """Full DJ circuit: H^n XH-ancilla, U_f, H^n, measure the n inputs."""
    qc = qk.QuantumCircuit(N_BITS + 1, N_BITS, name="deutsch-jozsa")
    qc.x(ANCILLA)
    qc.h(range(N_BITS + 1))
    qc.compose(oracle, inplace=True)
    qc.h(range(N_BITS))
    qc.measure(range(N_BITS), range(N_BITS))
    return qc


def all_zero_probability(oracle: qk.QuantumCircuit) -> float:
    """P(measure 0...0 on the n input bits), from a statevector."""
    qc = qk.QuantumCircuit(N_BITS + 1)
    qc.x(ANCILLA)
    qc.h(range(N_BITS + 1))
    qc.compose(oracle, inplace=True)
    qc.h(range(N_BITS))
    probs = qk.quantum_info.Statevector.from_instruction(qc).probabilities_dict()
    # Little-endian: input bits are the rightmost N_BITS of the (n+1)-bit string.
    p = 0.0
    for bits, pr in probs.items():
        if bits[-N_BITS:] == "0" * N_BITS:
            p += float(pr)
    return p


def verdict(zero_prob: float) -> str:
    return "constant" if zero_prob > 0.5 else "balanced"


def main() -> None:
    print(f"Deutsch–Jozsa, n={N_BITS} (one query vs ≤ {2 ** (N_BITS - 1) + 1} classically)\n")
    backend = AerSimulator()

    for name, (promise, factory) in ORACLES.items():
        oracle = factory()
        p0 = all_zero_probability(oracle)
        guess = verdict(p0)
        flag = "OK" if guess == promise else "WRONG"
        print(f"{name:18} promise={promise:8}  P(|00>)={p0:.3f}  guess={guess:8}  {flag}")

        qc = deutsch_jozsa_circuit(oracle)
        counts = backend.run(qk.transpile(qc, backend), shots=1024).result().get_counts()
        top = sorted(counts.items(), key=lambda kv: -kv[1])[:4]
        hist = "  ".join(f"|{bits}> {n}" for bits, n in top)
        print(f"{'':18} shots: {hist}")

    print("\nexample circuit (balanced parity oracle)")
    print(deutsch_jozsa_circuit(oracle_parity()).draw(output="text"))


if __name__ == "__main__":
    main()
