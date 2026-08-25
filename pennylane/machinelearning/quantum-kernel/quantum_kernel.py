#!/usr/bin/env python3
"""Quantum kernel methods for classification.

Uses PennyLane's qml.kernels module to compute a quantum kernel matrix
on the moons dataset.  A kernel SVM (via sklearn SVC with precomputed
kernel) is trained on the quantum kernel to classify data.

The kernel measures overlap fidelity:
  K(x1, x2) = |⟨0|U†(x1) U(x2)|0⟩|²
"""

import pennylane as qml
import numpy as np
from sklearn.datasets import make_moons
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler

N_FEATURES = 2
dev = qml.device("default.qubit", wires=N_FEATURES)


@qml.qnode(dev)
def kernel_circuit(x1, x2):
    qml.AngleEmbedding(x2, wires=range(N_FEATURES), rotation="Y")
    qml.adjoint(qml.AngleEmbedding)(x1, wires=range(N_FEATURES), rotation="Y")
    return qml.probs(wires=range(N_FEATURES))


def quantum_kernel(X1, X2):
    K = np.zeros((len(X1), len(X2)))
    for i, x1 in enumerate(X1):
        for j, x2 in enumerate(X2):
            probs = kernel_circuit(x1, x2)
            K[i, j] = probs[0]
    return K


def main() -> None:
    print("Quantum kernel SVM — moons dataset")

    X_raw, Y_raw = make_moons(n_samples=60, noise=0.15, random_state=0)
    X = X_raw[:40].astype(float)
    Y = Y_raw[:40].astype(float)
    X_test = X_raw[40:].astype(float)
    Y_test = Y_raw[40:].astype(float)

    scaler = MinMaxScaler(feature_range=(-np.pi / 2, np.pi / 2))
    X = scaler.fit_transform(X)
    X_test = scaler.transform(X_test)

    print(f"train={len(X)}  test={len(X_test)}")
    print("computing train kernel matrix...")
    K_train = quantum_kernel(X, X)
    print(f"  shape={K_train.shape}  range=[{K_train.min():.4f}, {K_train.max():.4f}]")

    print("computing test kernel matrix...")
    K_test = quantum_kernel(X_test, X)
    print(f"  shape={K_test.shape}")

    clf = SVC(kernel="precomputed", C=5.0)
    clf.fit(K_train, Y)

    train_acc = clf.score(K_train, Y)
    test_acc = clf.score(K_test, Y_test)
    print()
    print(f"train accuracy: {train_acc:.1%}")
    print(f"test accuracy:  {test_acc:.1%}")

    preds = clf.predict(K_test)
    print()
    print("predictions vs labels:")
    for i in range(len(X_test)):
        mark = "" if preds[i] == Y_test[i] else "  <-- WRONG"
        print(f"  x=[{X_test[i, 0]:+.3f}, {X_test[i, 1]:+.3f}]  "
              f"pred={int(preds[i])}  true={int(Y_test[i])}{mark}")


if __name__ == "__main__":
    main()
