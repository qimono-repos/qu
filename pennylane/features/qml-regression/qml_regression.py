#!/usr/bin/env python3
import pennylane as qml
import numpy as np

N_QUBITS = 2
N_LAYERS = 3
dev = qml.device("default.qubit", wires=N_QUBITS)

X_TRAIN = np.linspace(0, 2 * np.pi, 12).reshape(-1, 1)
Y_TRAIN = np.sin(X_TRAIN[:, 0])


@qml.qnode(dev, diff_method="parameter-shift")
def regressor(weights, x):
    qml.AngleEmbedding(x, wires=range(N_QUBITS), rotation="Y")
    for layer in range(N_LAYERS):
        for w in range(N_QUBITS):
            qml.RY(weights[layer, w, 0], wires=w)
            qml.RZ(weights[layer, w, 1], wires=w)
        qml.CNOT(wires=[0, 1])
    return qml.expval(qml.Z(0))


def cost(weights):
    predictions = np.array([regressor(weights, x) for x in X_TRAIN])
    return np.mean((predictions - Y_TRAIN) ** 2)


def main() -> None:
    print("QNN regression — sine wave")
    print(f"training points: {len(X_TRAIN)}")
    print()

    rng = np.random.default_rng(1)
    weights = rng.normal(0, 0.5, size=(N_LAYERS, N_QUBITS, 2))

    opt = qml.AdamOptimizer(stepsize=0.05)
    for step in range(1, 101):
        weights = opt.step(cost, weights)
        if step % 20 == 0:
            c = cost(weights)
            print(f"  step {step:3d}  mse={c:.6f}")

    print()
    print("predictions vs target:")
    x_test = np.linspace(0, 2 * np.pi, 8).reshape(-1, 1)
    y_test = np.sin(x_test[:, 0])
    preds = np.array([regressor(weights, x) for x in x_test])
    for xi, yi, pi in zip(x_test[:, 0], y_test, preds):
        bar_len = int(abs(pi) * 20)
        bar = "+" * bar_len if pi > 0 else "-" * bar_len
        print(f"  x={xi:.2f}  sin={yi:+.4f}  qnn={pi:+.4f}  {bar}")


if __name__ == "__main__":
    main()
