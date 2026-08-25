import cudaq
import numpy as np


@cudaq.kernel
def zero_zero():
    qubits = cudaq.qvector(2)


@cudaq.kernel
def zero_one():
    qubits = cudaq.qvector(2)
    x(qubits[0])


@cudaq.kernel
def one_zero():
    qubits = cudaq.qvector(1)
    x(qubits[0])
    q2 = cudaq.qvector(1)


@cudaq.kernel
def one_one():
    qubits = cudaq.qvector(2)
    x(qubits[0])
    x(qubits[1])


@cudaq.kernel
def product_state():
    qubits = cudaq.qvector(2)
    h(qubits[0])


if __name__ == "__main__":
    labels = ["|00>", "|01>", "|10>", "|11>"]
    kernels = [zero_zero, zero_one, one_zero, one_one]

    for label, kernel in zip(labels, kernels):
        result = cudaq.sample(kernel, shots_count=100)
        sv = np.array(cudaq.get_state(kernel))
        print(f"{label}:  probs={[f'{p:.2f}' for p in np.abs(sv)**2]}")
        for bitstring, count in result.items():
            print(f"  measured |{bitstring}>: {count}/100")

    print("\n=== |+0> tensor product (H on q0, |0> on q1) ===")
    result = cudaq.sample(product_state, shots_count=1000)
    sv = np.array(cudaq.get_state(product_state))
    probs = np.abs(sv) ** 2
    print(f"Statevector probs: {[f'{p:.4f}' for p in probs]}")
    for bitstring, count in result.items():
        print(f"  |{bitstring}>: {count}")
