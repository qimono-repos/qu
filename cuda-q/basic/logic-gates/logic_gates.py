import cudaq
import numpy as np


@cudaq.kernel
def apply_x():
    qubit = cudaq.qvector(1)
    x(qubit[0])


@cudaq.kernel
def apply_y():
    qubit = cudaq.qvector(1)
    y(qubit[0])


@cudaq.kernel
def apply_z():
    qubit = cudaq.qvector(1)
    z(qubit[0])


@cudaq.kernel
def apply_h():
    qubit = cudaq.qvector(1)
    h(qubit[0])


@cudaq.kernel
def apply_s():
    qubit = cudaq.qvector(1)
    h(qubit[0])
    s(qubit[0])


@cudaq.kernel
def apply_t():
    qubit = cudaq.qvector(1)
    h(qubit[0])
    t(qubit[0])


def show_statevector(name: str, kernel) -> None:
    sv = cudaq.get_state(kernel)
    amps = np.array(sv)
    probs = np.abs(amps) ** 2
    print(f"{name}:  |0>={amps[0]:+.4f}  |1>={amps[1]:+.4f}  "
          f"P(|0>)={probs[0]:.4f}  P(|1>)={probs[1]:.4f}")


if __name__ == "__main__":
    show_statevector("X gate (on |0>)", apply_x)
    show_statevector("Y gate (on |0>)", apply_y)
    show_statevector("Z gate (on |0>)", apply_z)
    show_statevector("H gate (on |0>)", apply_h)
    show_statevector("S gate (on |+>)", apply_s)
    show_statevector("T gate (on |+>)", apply_t)
