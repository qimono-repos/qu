#!/usr/bin/env python3
import pennylane as qml
import numpy as np

N_QUBITS = 4
dev = qml.device("default.qubit", wires=N_QUBITS)


@qml.qnode(dev)
def qft_circuit():
    qml.Hadamard(wires=0)
    qml.CRZ(np.pi / 2, wires=[1, 0])
    qml.CRZ(np.pi / 4, wires=[2, 0])
    qml.CRZ(np.pi / 8, wires=[3, 0])

    qml.Hadamard(wires=1)
    qml.CRZ(np.pi / 2, wires=[2, 1])
    qml.CRZ(np.pi / 4, wires=[3, 1])

    qml.Hadamard(wires=2)
    qml.CRZ(np.pi / 2, wires=[3, 2])

    qml.Hadamard(wires=3)

    qml.SWAP(wires=[0, 3])
    qml.SWAP(wires=[1, 2])
    return qml.probs(wires=range(N_QUBITS))


def main() -> None:
    print("Quantum Fourier Transform on 4 qubits")
    print()
    print(qml.draw(qft_circuit)())
    print()

    dev_full = qml.device("default.qubit", wires=N_QUBITS)

    @qml.qnode(dev_full)
    def qft_on_state(state):
        qml.BasisState(state, wires=range(N_QUBITS))
        qml.Hadamard(wires=0)
        qml.CRZ(np.pi / 2, wires=[1, 0])
        qml.CRZ(np.pi / 4, wires=[2, 0])
        qml.CRZ(np.pi / 8, wires=[3, 0])
        qml.Hadamard(wires=1)
        qml.CRZ(np.pi / 2, wires=[2, 1])
        qml.CRZ(np.pi / 4, wires=[3, 1])
        qml.Hadamard(wires=2)
        qml.CRZ(np.pi / 2, wires=[3, 2])
        qml.Hadamard(wires=3)
        qml.SWAP(wires=[0, 3])
        qml.SWAP(wires=[1, 2])
        return qml.state()

    dim = 2**N_QUBITS
    matrix = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        state = list(map(int, format(col, f"0{N_QUBITS}b")))
        matrix[:, col] = qft_on_state(state)

    print(f"QFT matrix ({dim}×{dim}):")
    print(np.round(matrix, 4))


if __name__ == "__main__":
    main()
