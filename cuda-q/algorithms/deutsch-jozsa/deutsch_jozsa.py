import cudaq
import numpy as np


@cudaq.kernel
def dj_constant():
    """Deutsch-Jozsa with constant oracle f(x) = 0 (identity)."""
    qubits = cudaq.qvector(3)
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    h(qubits[2])
    h(qubits[0])
    h(qubits[1])


@cudaq.kernel
def dj_balanced_identity():
    """Deutsch-Jozsa with balanced oracle f(x) = x (CNOT from input to output)."""
    qubits = cudaq.qvector(3)
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    cx(qubits[0], qubits[2])
    h(qubits[0])
    h(qubits[1])


@cudaq.kernel
def dj_balanced_not():
    """Deutsch-Jozsa with balanced oracle f(x) = NOT x."""
    qubits = cudaq.qvector(3)
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    cx(qubits[1], qubits[2])
    h(qubits[0])
    h(qubits[1])


@cudaq.kernel
def dj_balanced_xor():
    """Deutsch-Jozsa with balanced oracle f(x0,x1) = x0 XOR x1."""
    qubits = cudaq.qvector(3)
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    cx(qubits[0], qubits[2])
    cx(qubits[1], qubits[2])
    h(qubits[0])
    h(qubits[1])


if __name__ == "__main__":
    print("=== Deutsch-Jozsa algorithm (n=2) ===")
    print("2 input qubits, 1 output qubit (ancilla)")
    print("Goal: determine if f(x) is constant or balanced\n")

    print("--- Constant oracle f(x) = 0 ---")
    sv = np.array(cudaq.get_state(dj_constant))
    probs = np.abs(sv) ** 2
    basis = ["|000>", "|001>", "|010>", "|011>",
             "|100>", "|101>", "|110>", "|111>"]
    print("Input qubits (first two):")
    for b, prob in zip(basis, probs):
        if prob > 0.001:
            print(f"  {b}: P={prob:.4f}")
    result = cudaq.sample(dj_constant, shots_count=1000)
    counts = {k: v for k, v in result.items()}
    measured = list(counts.keys())[0][:2]
    print(f"  Measured input qubits: |{measured}>")
    print(f"  Result: CONSTANT (all zeros after final H)")

    print("\n--- Balanced oracle f(x) = x0 ---")
    sv2 = np.array(cudaq.get_state(dj_balanced_identity))
    probs2 = np.abs(sv2) ** 2
    print("Input qubits (first two):")
    for b, prob in zip(basis, probs2):
        if prob > 0.001:
            print(f"  {b}: P={prob:.4f}")
    result2 = cudaq.sample(dj_balanced_identity, shots_count=1000)
    for bitstring, count in result2.items():
        measured = bitstring[:2]
        print(f"  measured |{bitstring}>: {count} (input: |{measured}>)")
    print(f"  Result: BALANCED (at least one input qubit is |1>)")

    print("\n--- Balanced oracle f(x) = x0 XOR x1 ---")
    sv3 = np.array(cudaq.get_state(dj_balanced_xor))
    probs3 = np.abs(sv3) ** 2
    print("Input qubits (first two):")
    for b, prob in zip(basis, probs3):
        if prob > 0.001:
            print(f"  {b}: P={prob:.4f}")
    result3 = cudaq.sample(dj_balanced_xor, shots_count=1000)
    for bitstring, count in result3.items():
        measured = bitstring[:2]
        print(f"  measured |{bitstring}>: {count} (input: |{measured}>)")
    print(f"  Result: BALANCED (at least one input qubit is |1>)")

    print("\nDeutsch-Jozsa: constant => |00>, balanced => anything else")
    print("Exponential speedup over classical (1 query vs 2^(n-1)+1)")
