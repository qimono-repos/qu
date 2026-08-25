import cudaq
import numpy as np


@cudaq.kernel
def oracle_11():
    """Oracle that marks |11> by applying a phase of -1 (CZ gate)."""
    qubits = cudaq.qvector(2)
    h(qubits[0])
    h(qubits[1])
    cz(qubits[0], qubits[1])
    h(qubits[0])
    h(qubits[1])


@cudaq.kernel
def oracle_10():
    """Oracle that marks |10> by flipping qubit 1, applying CZ, then flipping back."""
    qubits = cudaq.qvector(2)
    h(qubits[0])
    h(qubits[1])
    x(qubits[1])
    cz(qubits[0], qubits[1])
    x(qubits[1])
    h(qubits[0])
    h(qubits[1])


@cudaq.kernel
def oracle_both_11_and_00():
    """Oracle that marks both |11> and |00>."""
    qubits = cudaq.qvector(2)
    h(qubits[0])
    h(qubits[1])
    cz(qubits[0], qubits[1])
    x(qubits[0])
    cz(qubits[0], qubits[1])
    x(qubits[0])
    h(qubits[0])
    h(qubits[1])


if __name__ == "__main__":
    print("=== Oracle basics: marking computational basis states ===\n")

    print("--- Oracle marking |11> ---")
    sv = np.array(cudaq.get_state(oracle_11))
    probs = np.abs(sv) ** 2
    basis = ["|00>", "|01>", "|10>", "|11>"]
    for b, amp, prob in zip(basis, sv, probs):
        print(f"  {b}: amp={amp:+.4f}  P={prob:.4f}")
    result = cudaq.sample(oracle_11, shots_count=1000)
    for bitstring, count in result.items():
        print(f"  measured |{bitstring}>: {count}")

    print("\n--- Oracle marking |10> ---")
    sv2 = np.array(cudaq.get_state(oracle_10))
    probs2 = np.abs(sv2) ** 2
    for b, amp, prob in zip(basis, sv2, probs2):
        print(f"  {b}: amp={amp:+.4f}  P={prob:.4f}")
    result2 = cudaq.sample(oracle_10, shots_count=1000)
    for bitstring, count in result2.items():
        print(f"  measured |{bitstring}>: {count}")

    print("\n--- Oracle marking |11> and |00> ---")
    sv3 = np.array(cudaq.get_state(oracle_both_11_and_00))
    probs3 = np.abs(sv3) ** 2
    for b, amp, prob in zip(basis, sv3, probs3):
        print(f"  {b}: amp={amp:+.4f}  P={prob:.4f}")
    result3 = cudaq.sample(oracle_both_11_and_00, shots_count=1000)
    for bitstring, count in result3.items():
        print(f"  measured |{bitstring}>: {count}")

    print("\nThe oracle flips the phase of the marked state(s).")
    print("When applied to a uniform superposition, this is the")
    print("key building block for Grover's search algorithm.")
