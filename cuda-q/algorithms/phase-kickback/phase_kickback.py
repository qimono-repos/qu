import cudaq
import numpy as np


@cudaq.kernel
def phase_kickback_cnot():
    """Phase kickback using CNOT: control in |+>, target in |->."""
    qubits = cudaq.qvector(2)
    h(qubits[0])
    x(qubits[1])
    h(qubits[1])
    cx(qubits[0], qubits[1])
    h(qubits[1])


@cudaq.kernel
def phase_kickback_z():
    """Phase kickback using CZ: eigenvalue -1 kicks back to control."""
    qubits = cudaq.qvector(2)
    h(qubits[0])
    x(qubits[1])
    h(qubits[1])
    cz(qubits[0], qubits[1])
    h(qubits[1])


@cudaq.kernel
def phase_kickback_toffoli():
    """Phase kickback with 3 qubits: two controls in |+>, one target in |->."""
    qubits = cudaq.qvector(3)
    h(qubits[0])
    h(qubits[1])
    x(qubits[2])
    h(qubits[2])
    x(qubits[0], qubits[1], qubits[2])
    h(qubits[2])


if __name__ == "__main__":
    print("=== Phase kickback demonstration ===\n")

    print("--- CNOT phase kickback ---")
    print("Control qubit: |+> = (|0> + |1>)/sqrt(2)")
    print("Target qubit:  |-> = (|0> - |1>)/sqrt(2)")
    sv = np.array(cudaq.get_state(phase_kickback_cnot))
    probs = np.abs(sv) ** 2
    basis = ["|00>", "|01>", "|10>", "|11>"]
    for b, amp, prob in zip(basis, sv, probs):
        if prob > 0.001:
            print(f"  {b}: amp={amp:+.4f}  P={prob:.4f}")
    print("  Result: |->  |-> — target unchanged, control got phase")
    result = cudaq.sample(phase_kickback_cnot, shots_count=1000)
    for bitstring, count in result.items():
        print(f"  measured |{bitstring}>: {count}")

    print("\n--- CZ phase kickback ---")
    print("CZ applies -1 phase to |11>. When target is |->,")
    print("the -1 eigenvalue kicks back to the control.")
    sv2 = np.array(cudaq.get_state(phase_kickback_z))
    probs2 = np.abs(sv2) ** 2
    for b, amp, prob in zip(basis, sv2, probs2):
        if prob > 0.001:
            print(f"  {b}: amp={amp:+.4f}  P={prob:.4f}")
    print("  Control qubit acquired a phase of -1")
    result2 = cudaq.sample(phase_kickback_z, shots_count=1000)
    for bitstring, count in result2.items():
        print(f"  measured |{bitstring}>: {count}")

    print("\n--- Toffoli phase kickback ---")
    print("Three qubits: two controls in |+>, target in |->.")
    print("The -1 eigenvalue of Toffoli kicks back to the control register.")
    sv3 = np.array(cudaq.get_state(phase_kickback_toffoli))
    probs3 = np.abs(sv3) ** 2
    basis3 = ["|000>", "|001>", "|010>", "|011>",
              "|100>", "|101>", "|110>", "|111>"]
    for b, amp, prob in zip(basis3, sv3, probs3):
        if prob > 0.001:
            print(f"  {b}: amp={amp:+.4f}  P={prob:.4f}")
    result3 = cudaq.sample(phase_kickback_toffoli, shots_count=1000)
    for bitstring, count in result3.items():
        print(f"  measured |{bitstring}>: {count}")

    print("\nPhase kickback is the core mechanism behind:")
    print("  - Deutsch-Jozsa algorithm")
    print("  - Grover's search algorithm")
    print("  - Quantum phase estimation")
