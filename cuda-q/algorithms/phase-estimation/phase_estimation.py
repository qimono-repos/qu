import cudaq
import numpy as np


@cudaq.kernel
def qpe_rz(theta: float):
    """Phase estimation for RZ(theta) using 2 count qubits.
    
    Circuit:
    - Count qubits 0,1 start in |+> (H gates)
    - Target qubit 2 starts in eigenstate |1>
    - Controlled-U^(2^k) from count k to target
    - Inverse QFT on count register
    - Measure count register
    """
    qubits = cudaq.qvector(4)
    x(qubits[3])
    h(qubits[0])
    h(qubits[1])
    crz(qubits[0], qubits[3], theta)
    crz(qubits[1], qubits[3], 2 * theta)
    swap(qubits[0], qubits[1])
    h(qubits[0])
    crz(qubits[0], qubits[1], -np.pi / 2)
    h(qubits[1])


@cudaq.kernel
def qpe_ry(theta: float):
    """Phase estimation for RY(theta) using 2 count qubits."""
    qubits = cudaq.qvector(4)
    x(qubits[3])
    h(qubits[0])
    h(qubits[1])
    cry(qubits[0], qubits[3], theta)
    cry(qubits[1], qubits[3], 2 * theta)
    swap(qubits[0], qubits[1])
    h(qubits[0])
    crz(qubits[0], qubits[1], -np.pi / 2)
    h(qubits[1])


if __name__ == "__main__":
    print("=== Quantum Phase Estimation (2 count qubits) ===\n")
    print("Goal: estimate eigenvalue e^(i*theta) of a unitary U")
    print("Using 2 count qubits, we can resolve 4 phase values\n")

    test_angles = [np.pi / 2, np.pi, 3 * np.pi / 2]
    for theta in test_angles:
        print(f"--- RZ({theta:.4f}) = RZ({np.degrees(theta):.1f} deg) ---")
        sv = np.array(cudaq.get_state(qpe_rz, theta))
        probs = np.abs(sv) ** 2
        basis = ["|0000>", "|0001>", "|0010>", "|0011>",
                 "|0100>", "|0101>", "|0110>", "|0111>",
                 "|1000>", "|1001>", "|1010>", "|1011>",
                 "|1100>", "|1101>", "|1110>", "|1111>"]
        print("Count qubit states:")
        for b, prob in zip(basis, probs):
            if prob > 0.001:
                count_val = int(b[1:3], 2)
                phase_est = count_val * 2 * np.pi / 4
                print(f"  {b}: P={prob:.4f}  "
                      f"estimated phase = {phase_est:.4f} rad")
        result = cudaq.sample(qpe_rz, theta, shots_count=1000)
        for bitstring, count in result.items():
            count_val = int(bitstring[0:2], 2)
            phase_est = count_val * 2 * np.pi / 4
            print(f"  measured |{bitstring}>: {count} "
                  f"(phase ~ {phase_est:.4f} rad = "
                  f"{np.degrees(phase_est):.1f} deg)")
        print()

    print("=== QPE with RY rotation ===\n")
    for theta in [np.pi / 4, np.pi / 2]:
        print(f"--- RY({theta:.4f}) = RY({np.degrees(theta):.1f} deg) ---")
        result = cudaq.sample(qpe_ry, theta, shots_count=1000)
        for bitstring, count in result.items():
            count_val = int(bitstring[0:2], 2)
            phase_est = count_val * 2 * np.pi / 4
            print(f"  measured |{bitstring}>: {count} "
                  f"(phase ~ {phase_est:.4f} rad)")
        print()

    print("QPE is the core subroutine of:")
    print("  - Shor's factoring algorithm")
    print("  - Quantum simulation (eigenvalue estimation)")
    print("  - HHL linear systems algorithm")
