#!/usr/bin/env python3
import pennylane as qml
import numpy as np

N_QUBITS = 2
N_LAYERS = 2
dev = qml.device("default.qubit", wires=N_QUBITS)

X_TRAIN = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
Y_TRAIN = np.array([0, 1, 1, 0], dtype=float)


@qml.qnode(dev, diff_method="parameter-shift")
def classifier(weights, x):
    qml.AngleEmbedding(x, wires=range(N_QUBITS), rotation="Y")
    for layer in range(N_LAYERS):
        for w in range(N_QUBITS):
            qml.RY(weights[layer, w, 0], wires=w)
            qml.RZ(weights[layer, w, 1], wires=w)
        qml.CNOT(wires=[0, 1])
    return qml.expval(qml.Z(0))


def cost(weights):
    predictions = np.array([classifier(weights, x) for x in X_TRAIN])
    return 0.5 * np.mean((predictions - Y_TRAIN) ** 2)


def accuracy(weights):
    predictions = np.array([
        1 if classifier(weights, x) < 0 else 0 for x in X_TRAIN
    ])
    return np.mean(predictions == Y_TRAIN)


def main() -> None:
    print("Variational classifier — XOR")
    print(f"training data: {list(zip(map(tuple, X_TRAIN), Y_TRAIN))}")
    print()

    rng = np.random.default_rng(0)
    weights = rng.normal(0, 0.3, size=(N_LAYERS, N_QUBITS, 2))

    opt = qml.AdamOptimizer(stepsize=0.1)
    for step in range(1, 51):
        weights = opt.step(cost, weights)
        if step % 10 == 0:
            c = cost(weights)
            a = accuracy(weights)
            print(f"  step {step:3d}  cost={c:.6f}  acc={a:.1%}")

    print()
    print("final predictions:")
    for x, y_true in zip(X_TRAIN, Y_TRAIN):
        raw = classifier(weights, x)
        y_pred = 1 if raw < 0 else 0
        mark = "" if y_pred == y_true else "  <-- WRONG"
        print(f"  {list(map(int, x))}  true={int(y_true)}  "
              f"raw={raw:+.4f}  pred={y_pred}{mark}")


if __name__ == "__main__":
    main()
