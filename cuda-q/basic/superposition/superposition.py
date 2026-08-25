import cudaq
import numpy as np


@cudaq.kernel
def hadamard_once():
    qubit = cudaq.qvector(1)
    h(qubit[0])


@cudaq.kernel
def hadamard_twice():
    qubit = cudaq.qvector(1)
    h(qubit[0])
    h(qubit[0])


if __name__ == "__main__":
    print("=== H|0> (superposition) ===")
    result = cudaq.sample(hadamard_once, shots_count=1000)
    for bitstring, count in result.items():
        print(f"  |{bitstring}>: {count}")

    sv = cudaq.get_state(hadamard_once)
    amps = np.array(sv)
    print(f"Statevector: |0>={amps[0]:.4f}  |1>={amps[1]:.4f}")

    print("\n=== HH|0> (back to |0>) ===")
    result2 = cudaq.sample(hadamard_twice, shots_count=1000)
    for bitstring, count in result2.items():
        print(f"  |{bitstring}>: {count}")

    sv2 = cudaq.get_state(hadamard_twice)
    amps2 = np.array(sv2)
    print(f"Statevector: |0>={amps2[0]:.4f}  |1>={amps2[1]:.4f}")
