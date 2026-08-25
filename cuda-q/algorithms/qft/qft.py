import cudaq
import numpy as np


@cudaq.kernel
def qft_3q(input_val: int):
    """3-qubit QFT. input_val encodes the input state via X gates."""
    qubits = cudaq.qvector(3)
    if (input_val & 1) != 0:
        x(qubits[0])
    if (input_val & 2) != 0:
        x(qubits[1])
    if (input_val & 4) != 0:
        x(qubits[2])
    h(qubits[0])
    crz(qubits[1], qubits[0], np.pi / 2)
    crz(qubits[2], qubits[0], np.pi / 4)
    h(qubits[1])
    crz(qubits[2], qubits[1], np.pi / 2)
    h(qubits[2])
    swap(qubits[0], qubits[2])


@cudaq.kernel
def qft_inverse_3q(input_val: int):
    """Inverse QFT (QFT^dagger) on 3 qubits."""
    qubits = cudaq.qvector(3)
    if (input_val & 1) != 0:
        x(qubits[0])
    if (input_val & 2) != 0:
        x(qubits[1])
    if (input_val & 4) != 0:
        x(qubits[2])
    swap(qubits[0], qubits[2])
    h(qubits[2])
    crz(qubits[2], qubits[1], -np.pi / 2)
    h(qubits[1])
    crz(qubits[2], qubits[0], -np.pi / 4)
    crz(qubits[1], qubits[0], -np.pi / 2)
    h(qubits[0])


if __name__ == "__main__":
    print("=== Quantum Fourier Transform (3 qubits) ===\n")

    basis = ["|000>", "|001>", "|010>", "|011>",
             "|100>", "|101>", "|110>", "|111>"]

    for val in range(8):
        sv = np.array(cudaq.get_state(qft_3q, val))
        probs = np.abs(sv) ** 2
        print(f"QFT|{val:03d}>:")
        for b, amp, prob in zip(basis, sv, probs):
            if prob > 0.001:
                print(f"  {b}: amp={amp:+.4f}+{np.imag(amp):+.4f}j  "
                      f"P={prob:.4f}")
        print()

    print("=== QFT * QFT^dagger = Identity verification ===\n")
    for val in range(4):
        sv = np.array(cudaq.get_state(qft_inverse_3q, val))
        probs = np.abs(sv) ** 2
        dominant = np.argmax(probs)
        print(f"QFT^dagger * QFT |{val:03d}> -> "
              f"|{dominant:03d}> (P={probs[dominant]:.4f})")

    print("\nThe QFT maps between computational and phase bases.")
    print("It is the quantum analog of the discrete Fourier transform.")
    print("Key application: Quantum Phase Estimation (QPE)")
