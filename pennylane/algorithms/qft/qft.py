#!/usr/bin/env python3
"""Quantum Fourier Transform on 3 qubits."""
import pennylane as qml
import numpy as np

N = 3
dev = qml.device("default.qubit", wires=N)


def qft_rotations(wires: list[int]) -> None:
    """Apply the QFT rotation gates for the given wire list."""
    n = len(wires)
    for i in range(n):
        qml.Hadamard(wires=wires[i])
        for j in range(i + 1, n):
            k = j - i
            qml.ctrl(qml.RZ, control=wires[j])(
                np.pi / (2**k), wires=wires[i]
            )


def qft_circuit() -> None:
    """Full QFT with reversal of output qubit order."""
    qft_rotations(list(range(N)))
    for i in range(N // 2):
        qml.SWAP(wires=[i, N - 1 - i])


@qml.qnode(dev)
def apply_qft(state: int) -> qml.typing.Result:
    """Prepare |state⟩ and apply QFT."""
    for i in range(N):
        if state & (1 << i):
            qml.PauliX(wires=i)
    qft_circuit()
    return qml.state()


@qml.qnode(dev)
def qft_matrix_check() -> qml.typing.Result:
    """Apply QFT to |0⟩ to verify the equal superposition output."""
    qft_circuit()
    return qml.state()


def main() -> None:
    print("=== Quantum Fourier Transform (3 qubits) ===")
    print()

    print("QFT circuit:")
    print(qml.draw(qft_matrix_check)())
    print()

    print("QFT|0⟩ should give equal superposition:")
    state0 = qft_matrix_check()
    expected = np.ones(2**N) / np.sqrt(2**N)
    print(f"  Amplitudes: {[f'{a:.4f}' for a in state0]}")
    print(f"  Match equal superposition: {np.allclose(np.abs(state0), np.abs(expected))}")
    print()

    print("QFT on computational basis states:")
    for s in range(2**N):
        state = apply_qft(s)
        bits = format(s, f"0{N}b")
        print(f"  QFT|{bits}⟩:")
        for i, amp in enumerate(state):
            if abs(amp) > 1e-10:
                ibits = format(i, f"0{N}b")
                print(f"    |{ibits}⟩: {amp:.4f}")
        print()


if __name__ == "__main__":
    main()
