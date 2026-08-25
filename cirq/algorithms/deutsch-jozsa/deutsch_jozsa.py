"""Deutsch-Jozsa algorithm: distinguish constant from balanced oracles, n=2."""

import cirq
import numpy as np


def constant_oracle_0(qubits: list[cirq.LineQubit]) -> list[cirq.Operation]:
    """Constant oracle f(x) = 0 for all x.  Do nothing."""
    return []


def constant_oracle_1(qubits: list[cirq.LineQubit]) -> list[cirq.Operation]:
    """Constant oracle f(x) = 1 for all x.  Flip the output qubit unconditionally."""
    return [cirq.X(qubits[-1])]


def balanced_oracle_id(qubits: list[cirq.LineQubit]) -> list[cirq.Operation]:
    """Balanced oracle f(x) = x0.  CNOT from input to output."""
    return [cirq.CNOT(qubits[0], qubits[-1])]


def balanced_oracle_xor(qubits: list[cirq.LineQubit]) -> list[cirq.Operation]:
    """Balanced oracle f(x) = x0 XOR x1.  CNOT from both inputs to output."""
    return [cirq.CNOT(qubits[0], qubits[-1]), cirq.CNOT(qubits[1], qubits[-1])]


def run_deutsch_jozsa(
    name: str, oracle_fn, n: int = 2
) -> None:
    """Run Deutsch-Jozsa with the given oracle and print the result."""
    qubits = cirq.LineQubit.range(n + 1)
    output = qubits[n]
    inputs = qubits[:n]

    circuit = cirq.Circuit(
        cirq.X(output),
        [cirq.H(q) for q in qubits],
        *oracle_fn(qubits),
        [cirq.H(q) for q in inputs],
    )

    print(f"--- {name} ---")
    print(circuit)

    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    sv = result.final_state_vector

    n_inputs = 2 ** n
    measured_zero = True
    for i in range(n_inputs):
        if abs(sv[i]) > 1e-6:
            measured_zero = False
            break

    if measured_zero:
        verdict = "CONSTANT (all outputs measured |0⟩)"
    else:
        verdict = "BALANCED (at least one |1⟩ measured)"

    print(f"  First {n_inputs} amplitudes (input register):")
    for i in range(n_inputs):
        print(f"    |{i:0{n}b}⟩: {sv[i]:.4f}")
    print(f"  → {verdict}\n")


def main() -> None:
    run_deutsch_jozsa("Constant f(x)=0", constant_oracle_0)
    run_deutsch_jozsa("Constant f(x)=1", constant_oracle_1)
    run_deutsch_jozsa("Balanced f(x)=x0", balanced_oracle_id)
    run_deutsch_jozsa("Balanced f(x)=x0⊕x1", balanced_oracle_xor)


if __name__ == "__main__":
    main()
