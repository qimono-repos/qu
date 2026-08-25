#!/usr/bin/env python3
import pennylane as qml

N_QUBITS = 2
dev = qml.device("default.qubit", wires=N_QUBITS)


@qml.qnode(dev)
def bell_state():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.probs(wires=range(N_QUBITS))


def main() -> None:
    print("Bell state |Φ+⟩ via PennyLane")
    print()
    print(qml.draw(bell_state)())
    print()
    probs = bell_state()
    labels = [f"|{i:0{N_QUBITS}b}⟩" for i in range(2**N_QUBITS)]
    for label, p in zip(labels, probs):
        print(f"  {label}  {p:.4f}")


if __name__ == "__main__":
    main()
