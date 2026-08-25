#!/usr/bin/env python3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)


@qml.qnode(dev, diff_method="parameter-shift")
def circuit_ps(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=0)
    return qml.expval(qml.Z(0))


@qml.qnode(dev, diff_method="backprop")
def circuit_bp(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=0)
    return qml.expval(qml.Z(0))


@qml.qnode(dev, diff_method="adjoint")
def circuit_ad(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=0)
    return qml.expval(qml.Z(0))


def main() -> None:
    params = np.array([0.7, 1.3], requires_grad=True)

    print("Gradient comparison on RY(RX(θ₀)|0⟩)")
    print(f"params = {params}")
    print()
    print(qml.draw(circuit_ps)(params))
    print()

    g_ps = qml.grad(circuit_ps)(params)
    g_bp = qml.grad(circuit_bp)(params)
    g_ad = qml.grad(circuit_ad)(params)

    print("Method           d/dθ₀       d/dθ₁")
    print(f"parameter-shift  {g_ps[0]:+.8f}  {g_ps[1]:+.8f}")
    print(f"backprop         {g_bp[0]:+.8f}  {g_bp[1]:+.8f}")
    print(f"adjoint          {g_ad[0]:+.8f}  {g_ad[1]:+.8f}")
    print()
    print(f"PS vs BP max diff: {np.max(np.abs(g_ps - g_bp)):.2e}")
    print(f"PS vs AD max diff: {np.max(np.abs(g_ps - g_ad)):.2e}")


if __name__ == "__main__":
    main()
