import cudaq
import numpy as np


@cudaq.kernel
def cnot_kernel():
    qubits = cudaq.qvector(2)
    h(qubits[0])
    cx(qubits[0], qubits[1])


@cudaq.kernel
def cz_kernel():
    qubits = cudaq.qvector(2)
    h(qubits[0])
    cz(qubits[0], qubits[1])


@cudaq.kernel
def cnot_no_superposition():
    qubits = cudaq.qvector(2)
    x(qubits[0])
    cx(qubits[0], qubits[1])


if __name__ == "__main__":
    print("=== CNOT (H|0> -> |0> + |1>) on control ===")
    result = cudaq.sample(cnot_kernel, shots_count=1000)
    sv = np.array(cudaq.get_state(cnot_kernel))
    probs = np.abs(sv) ** 2
    print(f"Statevector probs: {[f'{p:.4f}' for p in probs]}")
    for bitstring, count in result.items():
        print(f"  |{bitstring}>: {count}")

    print("\n=== CZ (H|0> -> |0> + |1>) on control ===")
    result2 = cudaq.sample(cz_kernel, shots_count=1000)
    sv2 = np.array(cudaq.get_state(cz_kernel))
    probs2 = np.abs(sv2) ** 2
    print(f"Statevector probs: {[f'{p:.4f}' for p in probs2]}")
    for bitstring, count in result2.items():
        print(f"  |{bitstring}>: {count}")

    print("\n=== CNOT with |1> control (deterministic flip) ===")
    result3 = cudaq.sample(cnot_no_superposition, shots_count=100)
    for bitstring, count in result3.items():
        print(f"  |{bitstring}>: {count}")
