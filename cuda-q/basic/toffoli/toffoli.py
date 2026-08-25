import cudaq
import numpy as np


@cudaq.kernel
def toffoli_one_one():
    qubits = cudaq.qvector(3)
    x(qubits[0])
    x(qubits[1])
    x(qubits[2])


@cudaq.kernel
def toffoli_control_flip():
    qubits = cudaq.qvector(3)
    x(qubits[0])
    x(qubits[1])


@cudaq.kernel
def toffoli_no_flip():
    qubits = cudaq.qvector(3)
    x(qubits[0])


if __name__ == "__main__":
    print("=== Toffoli gate (CCX) on |110> ===")
    result = cudaq.sample(toffoli_control_flip, shots_count=100)
    sv = np.array(cudaq.get_state(toffoli_control_flip))
    probs = np.abs(sv) ** 2
    basis = ["|000>", "|001>", "|010>", "|011>",
             "|100>", "|101>", "|110>", "|111>"]
    print("Before Toffoli:")
    for b, prob in zip(basis, probs):
        if prob > 0.001:
            print(f"  {b}: P={prob:.4f}")

    @cudaq.kernel
    def toffoli_on_110():
        qubits = cudaq.qvector(3)
        x(qubits[0])
        x(qubits[1])
        x(qubits[0], qubits[1], qubits[2])

    result2 = cudaq.sample(toffoli_on_110, shots_count=100)
    sv2 = np.array(cudaq.get_state(toffoli_on_110))
    probs2 = np.abs(sv2) ** 2
    print("\nAfter Toffoli:")
    for b, prob in zip(basis, probs2):
        if prob > 0.001:
            print(f"  {b}: P={prob:.4f}")
    for bitstring, count in result2.items():
        print(f"  measured |{bitstring}>: {count}")
    print("(|110> -> |111>: both controls are |1>, target flips)")

    print("\n=== Toffoli gate on |100> ===")

    @cudaq.kernel
    def toffoli_on_100():
        qubits = cudaq.qvector(3)
        x(qubits[0])
        x(qubits[0], qubits[1], qubits[2])

    sv3 = np.array(cudaq.get_state(toffoli_on_100))
    probs3 = np.abs(sv3) ** 2
    print("After Toffoli:")
    for b, prob in zip(basis, probs3):
        if prob > 0.001:
            print(f"  {b}: P={prob:.4f}")
    print("(|100> -> |100>: only one control is |1>, no flip)")
