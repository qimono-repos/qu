#!/usr/bin/env python3
"""Quantum regression on simple sine data.

A parameterised quantum circuit learns to approximate sin(x) on [0, 2*pi].
The circuit uses angle embedding (RY), trainable RY/RZ layers with CNOT
entanglement, and outputs the Z-expectation as the predicted value.
Training uses PennyLane's backpropagation differentiation via Adam.
"""

import pennylane as qml

N_QUBITS = 2
N_LAYERS = 6
dev = qml.device("default.qubit", wires=N_QUBITS)


@qml.qnode(dev, diff_method="backprop")
def circuit(weights, x):
    qml.AngleEmbedding(x, wires=range(N_QUBITS), rotation="Y")
    for layer in range(N_LAYERS):
        for w in range(N_QUBITS):
            qml.RY(weights[layer, w, 0], wires=w)
            qml.RZ(weights[layer, w, 1], wires=w)
        qml.CNOT(wires=[0, 1])
    return qml.expval(qml.Z(0))


def mse_loss(weights):
    predictions = qml.math.stack([circuit(weights, x) for x in X_TRAIN])
    return qml.math.mean((predictions - Y_TRAIN) ** 2)


def main() -> None:
    print("QNN regression — sine wave")

    rng = qml.numpy.random.default_rng(7)
    global X_TRAIN, Y_TRAIN
    X_TRAIN = qml.numpy.array(
        rng.uniform(0, 2 * qml.numpy.pi, size=20).reshape(-1, 1),
        requires_grad=False,
    )
    Y_TRAIN = qml.numpy.array(
        qml.math.sin(X_TRAIN[:, 0]),
        requires_grad=False,
    )

    X_test = qml.numpy.linspace(0, 2 * qml.numpy.pi, 12).reshape(-1, 1)
    Y_test = qml.math.sin(X_test[:, 0])

    print(f"train={len(X_TRAIN)}  test={len(X_test)}")
    print()

    weights = qml.numpy.array(
        rng.normal(0, 0.5, size=(N_LAYERS, N_QUBITS, 2)),
        requires_grad=True,
    )

    print(f"initial  mse={float(mse_loss(weights)):.6f}")

    opt = qml.AdamOptimizer(stepsize=0.05)
    for step in range(1, 101):
        weights = opt.step(mse_loss, weights)
        if step % 20 == 0:
            mse = float(mse_loss(weights))
            print(f"  step {step:3d}  mse={mse:.6f}")

    print()
    preds = qml.math.stack([circuit(weights, x) for x in X_test])
    test_mse = float(qml.math.mean((preds - Y_test) ** 2))
    print(f"test mse: {test_mse:.6f}")
    print()
    print("predictions vs target:")
    for xi, yi, pi in zip(X_test[:, 0], Y_test, preds):
        bar_len = int(abs(float(pi)) * 20)
        bar = "+" * bar_len if float(pi) > 0 else "-" * bar_len
        print(f"  x={float(xi):5.2f}  sin={float(yi):+.4f}  "
              f"qnn={float(pi):+.4f}  {bar}")


if __name__ == "__main__":
    main()
