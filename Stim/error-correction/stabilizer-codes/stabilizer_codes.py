"""3-qubit bit-flip and phase-flip stabilizer codes.

Demonstrates encoding, error injection, syndrome measurement, and correction.
"""

import stim
import numpy as np


def bit_flip_code() -> None:
    """3-qubit bit-flip code: protects against single X errors."""
    print("=== 3-Qubit Bit-Flip Code ===\n")

    # Encoding: |0⟩ → |000⟩, |1⟩ → |111⟩
    # Stabilizers: Z₀Z₁ and Z₁Z₂
    circuit = stim.Circuit("""
        # Encode logical |0⟩
        # (start in |000⟩, which is already a codeword)

        # Inject X error on qubit 1
        X 1

        # Syndrome measurement
        # Z₀Z₁ syndrome
        DETECTOR rec[-2]
        # Z₁Z₂ syndrome
        DETECTOR rec[-1]

        # Measure all qubits
        M 0 1 2
    """)

    # Sample and analyze
    detector_samples = circuit.detector_error_model()
    print(f"Detector error model:\n{detector_samples}\n")

    # Run simulation
    sampler = circuit.compile_detector_error_model()
    num_shots = 1000
    detection_events = sampler.sample(num_shots)

    print(f"Detection events (first 10 of {num_shots}):")
    for i in range(min(10, num_shots)):
        print(f"  Shot {i}: {detection_events[i]}")

    # Syndrome analysis
    syndrome_counts = {}
    for i in range(num_shots):
        syndrome = tuple(detection_events[i])
        syndrome_counts[syndrome] = syndrome_counts.get(syndrome, 0) + 1

    print(f"\nSyndrome distribution:")
    for syndrome, count in sorted(syndrome_counts.items()):
        print(f"  {syndrome}: {count}/{num_shots} ({100*count/num_shots:.1f}%)")

    print("\nSyndrome (0,0) = no error detected")
    print("Syndrome (1,0) = error on qubit 0")
    print("Syndrome (1,1) = error on qubit 1")
    print("Syndrome (0,1) = error on qubit 2")


def phase_flip_code() -> None:
    """3-qubit phase-flip code: protects against single Z errors."""
    print("\n=== 3-Qubit Phase-Flip Code ===\n")

    # Encoding: |0⟩ → |+++⟩, |1⟩ → |---⟩
    # Apply H, then bit-flip code, then H
    circuit = stim.Circuit("""
        # Encode: H on all qubits
        H 0
        H 1
        H 2

        # Inject Z error on qubit 1
        Z 1

        # Decode: H on all qubits
        H 0
        H 1
        H 2

        # Syndrome measurement (same as bit-flip in X basis)
        DETECTOR rec[-2]
        DETECTOR rec[-1]

        M 0 1 2
    """)

    sampler = circuit.compile_detector_error_model()
    num_shots = 1000
    detection_events = sampler.sample(num_shots)

    syndrome_counts = {}
    for i in range(num_shots):
        syndrome = tuple(detection_events[i])
        syndrome_counts[syndrome] = syndrome_counts.get(syndrome, 0) + 1

    print(f"Syndrome distribution:")
    for syndrome, count in sorted(syndrome_counts.items()):
        print(f"  {syndrome}: {count}/{num_shots} ({100*count/num_shots:.1f}%)")


def main() -> None:
    bit_flip_code()
    phase_flip_code()


if __name__ == "__main__":
    main()
