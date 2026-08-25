#!/usr/bin/env python3
"""Quantum neural network classifier on the moons dataset.

A 2-qubit parameterised circuit with data re-uploading is trained on
the sklearn moons dataset using PennyLane's backpropagation.  Features
are re-encoded after each variational layer so the circuit can build
a rich, nonlinear decision boundary.
"""

import pennylane as qml
from sklearn.datasets import make_moons

N_QUBITS = 2
N_LAYERS = 4
dev = qml.device("default.qubit", wires=N_QUBITS)


@qml.qnode(dev, diff_method="backprop")
def circuit(weights, x):
    for layer in range(N_LAYERS):
        qml.AngleEmbedding(x, wires=range(N_QUBITS), rotation="Y")
        for w in range(N_QUBITS):
            qml.RY(weights[layer, w, 0], wires=w)
            qml.RZ(weights[layer, w, 1], wires=w)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 0])
    return qml.expval(qml.Z(0))


def cost(weights):
    predictions = qml.math.stack([circuit(weights, x) for x in X_TRAIN])
    labels = 2.0 * Y_TRAIN - 1.0
    return 0.5 * qml.math.mean((predictions - labels) ** 2)


def accuracy(weights):
    predictions = qml.math.stack([circuit(weights, x) for x in X_TRAIN])
    preds = qml.math.cast(predictions >= 0, int)
    return qml.math.mean(preds == Y_TRAIN)


def main() -> None:
    print("QNN classifier — moons dataset")
    X_raw, Y_raw = make_moons(n_samples=80, noise=0.15, random_state=0)
    global X_TRAIN, Y_TRAIN
    X_TRAIN = qml.numpy.array(X_raw[:60].astype(float), requires_grad=False)
    Y_TRAIN = qml.numpy.array(Y_raw[:60].astype(float), requires_grad=False)
    X_test = X_raw[60:].astype(float)
    Y_test = Y_raw[60:].astype(float)
    print(f"train={len(X_TRAIN)}  test={len(X_test)}")
    print()

    rng = qml.numpy.random.default_rng(42)
    weights = qml.numpy.array(
        rng.normal(0, 0.3, size=(N_LAYERS, N_QUBITS, 2)),
        requires_grad=True,
    )

    print(f"initial  cost={float(cost(weights)):.4f}  "
          f"acc={float(accuracy(weights)):.1%}")

    opt = qml.AdamOptimizer(stepsize=0.1)
    for step in range(1, 81):
        weights = opt.step(cost, weights)
        if step % 20 == 0:
            c = float(cost(weights))
            a = float(accuracy(weights))
            print(f"  step {step:3d}  cost={c:.4f}  acc={a:.1%}")

    print()
    raw = qml.math.stack([circuit(weights, x) for x in X_test])
    preds = qml.math.cast(raw >= 0, int)
    test_acc = float(qml.math.mean(preds == Y_test))
    print(f"test accuracy: {test_acc:.1%}")
    print()
    print("predictions vs labels:")
    for i in range(len(X_test)):
        mark = "" if preds[i] == Y_test[i] else "  <-- WRONG"
        print(f"  x=[{X_test[i, 0]:+.3f}, {X_test[i, 1]:+.3f}]  "
              f"raw={float(raw[i]):+.4f}  pred={int(preds[i])}  "
              f"true={int(Y_test[i])}{mark}")


if __name__ == "__main__":
    main()
