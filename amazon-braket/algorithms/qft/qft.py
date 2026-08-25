#!/usr/bin/env python3
"""Quantum Fourier Transform on 3 qubits.

The QFT maps a computational basis state |j> to a uniform superposition
of all basis states with phases that encode j:

  QFT|j> = 1/sqrt(N) sum_k exp(2*pi*i*j*k/N) |k>

We build the QFT from Hadamard and controlled-phase gates, apply it
to |5> (binary 101), and verify the output amplitudes match the
analytical DFT formula.  We then verify the QFT-IQFT identity on all
eight 3-qubit basis states.
"""

from __future__ import annotations

import cmath

from braket.circuits import Circuit, ResultType
from braket.devices import LocalSimulator

N_QUBITS = 3
N_STATES = 2**N_QUBITS


def sv_probs(circuit: Circuit) -> tuple[list[complex], list[float]]:
    """Run circuit with statevector + probability result types."""
    circuit.add_result_type(ResultType.StateVector())
    circuit.add_result_type(ResultType.Probability())
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    sv = [complex(a) for a in result.result_types[0].value]
    probs = [float(p) for p in result.result_types[1].value]
    return sv, probs


def prepare_basis(circuit: Circuit, j: int, n: int = N_QUBITS) -> None:
    """Prepare computational basis state |j> using Braket big-endian convention.

    Braket state vector index = q0*2^{n-1} + q1*2^{n-2} + ... + q_{n-1}*2^0,
    so qubit 0 is the MSB.  Setting qubit i to 1 contributes 2^{n-1-i}.
    """
    for i in range(n):
        if (j >> (n - 1 - i)) & 1:
            circuit.x(i)


def qft_circuit(n: int = N_QUBITS) -> Circuit:
    """Build the QFT circuit on n qubits.

    The circuit applies Hadamard and controlled-phase gates in the standard
    textbook order, with a final SWAP to match Braket's big-endian qubit
    convention.  The resulting unitary equals the DFT matrix: column j
    gives the QFT of |j>.
    """
    circuit = Circuit()
    for i in range(n):
        circuit.h(i)
        for j in range(i + 1, n):
            k = j - i + 1
            angle = 2.0 * cmath.pi / (2**k)
            circuit.cphaseshift(j, i, angle)
    for i in range(n // 2):
        circuit.swap(i, n - 1 - i)
    return circuit


def iqft_circuit(n: int = N_QUBITS) -> Circuit:
    """Build the inverse QFT circuit on n qubits.

    Obtained by reversing the QFT gate sequence, negating all phase angles,
    and keeping SWAPs (self-inverse) at the beginning.  This exactly
    inverts the QFT:  QFT @ IQFT = IQFT @ QFT = I.
    """
    circuit = Circuit()
    for i in range(n // 2):
        circuit.swap(i, n - 1 - i)
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            k = j - i + 1
            angle = -2.0 * cmath.pi / (2**k)
            circuit.cphaseshift(j, i, angle)
        circuit.h(i)
    return circuit


def expected_qft(j: int, n: int = N_QUBITS) -> list[complex]:
    """Compute expected QFT amplitudes for input |j>:  w^{jk}/sqrt(N)."""
    N = 2**n
    return [cmath.exp(2j * cmath.pi * j * k / N) / N**0.5 for k in range(N)]


def demo_qft_on_five() -> None:
    """Apply QFT to |5> = |101> and verify against the DFT formula."""
    j = 5
    print(f"=== QFT on |{j}> ({N_QUBITS} qubits) ===")

    circuit = Circuit()
    prepare_basis(circuit, j)
    circuit.add_circuit(qft_circuit())

    sv, probs = sv_probs(circuit)
    expected = expected_qft(j)

    print("k  | measured amp       | expected amp         | |amp|^2")
    for k in range(N_STATES):
        bits = format(k, f"0{N_QUBITS}b")
        m = sv[k]
        e = expected[k]
        p = probs[k]
        match = "ok" if abs(m - e) < 1e-6 else "MISMATCH"
        print(f"|{bits}>  {m.real:+.4f}{m.imag:+.4f}i  "
              f"{e.real:+.4f}{e.imag:+.4f}i  {p:.4f}  {match}")
    print()


def demo_qft_identity() -> None:
    """QFT followed by IQFT should return the original state."""
    print("=== QFT then IQFT = identity ===")
    all_ok = True
    for j in range(N_STATES):
        circuit = Circuit()
        prepare_basis(circuit, j)
        circuit.add_circuit(qft_circuit())
        circuit.add_circuit(iqft_circuit())

        sv, _ = sv_probs(circuit)
        out_idx = max(range(len(sv)), key=lambda i: abs(sv[i]))
        ok = out_idx == j
        all_ok = all_ok and ok
        status = "ok" if ok else "FAIL"
        print(f"  |{j}> -> |{out_idx}>  {status}")
    print(f"All passed: {all_ok}\n")


def demo_unitary() -> None:
    """Show that the QFT unitary equals the DFT matrix."""
    print("=== QFT unitary = DFT matrix ===")
    device = LocalSimulator()

    def matrix_from(fn: "callable[[Circuit], None]") -> list[list[complex]]:
        cols: list[list[complex]] = []
        for j in range(N_STATES):
            c = Circuit()
            prepare_basis(c, j)
            fn(c)
            c.add_result_type(ResultType.StateVector())
            sv = device.run(c, shots=0).result().result_types[0].value
            cols.append([complex(a) for a in sv])
        return [[cols[c][r] for c in range(N_STATES)] for r in range(N_STATES)]

    qft_mat = matrix_from(lambda c: c.add_circuit(qft_circuit()))
    expected_mat = [[expected_qft(j)[k] for j in range(N_STATES)]
                    for k in range(N_STATES)]

    max_err = max(abs(qft_mat[r][c] - expected_mat[r][c])
                  for r in range(N_STATES) for c in range(N_STATES))
    print(f"Max element-wise error: {max_err:.2e}")
    print(f"QFT unitary matches DFT: {max_err < 1e-6}\n")


def main() -> None:
    demo_qft_on_five()
    demo_qft_identity()
    demo_unitary()


if __name__ == "__main__":
    main()
