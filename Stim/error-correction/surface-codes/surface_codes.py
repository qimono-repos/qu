"""Distance-3 surface code (repetition code) using Stim.

Demonstrates encoding, error detection, and syndrome analysis.
"""

import stim
import numpy as np


def repetition_code() -> None:
    """Distance-3 repetition code using Stim's built-in generator."""
    print("=== Distance-3 Repetition Code ===\n")

    # Use Stim's built-in repetition code generator
    circuit = stim.Circuit.generated(
        "repetition_code:memory",
        distance=3,
        rounds=1,
        after_clifford_depolarization=0.0,
    )

    print(f"Circuit has {circuit.num_qubits} qubits")
    print(f"Circuit has {circuit.num_detectors} detectors")
    print(f"Circuit has {circuit.num_observables} observables\n")

    # Sample without noise
    num_shots = 1000
   compiled_sampler = circuit.compile_detector_error_model()
    detection_events = compiled_sampler.sample(num_shots)

    # Analyze detection events
    print("Detection event statistics (no noise):")
    for det_idx in range(detection_events.shape[1]):
        count = np.sum(detection_events[:, det_idx])
        print(f"  Detector {det_idx}: {count}/{num_shots} triggered ({100*count/num_shots:.1f}%)")

    # With noise
    print("\n--- With depolarizing noise (p=0.01) ---\n")
    noisy_circuit = stim.Circuit.generated(
        "repetition_code:memory",
        distance=3,
        rounds=1,
        after_clifford_depolarization=0.01,
        before_round_data_depolarization=0.01,
    )

    compiled_noisy = noisy_circuit.compile_detector_error_model()
    detection_events_noisy = compiled_noisy.sample(num_shots)

    print("Detection event statistics (noisy):")
    for det_idx in range(detection_events_noisy.shape[1]):
        count = np.sum(detection_events_noisy[:, det_idx])
        print(f"  Detector {det_idx}: {count}/{num_shots} triggered ({100*count/num_shots:.1f}%)")


def detector_error_model() -> None:
    """Analyze the detector error model of the repetition code."""
    print("\n=== Detector Error Model ===\n")

    circuit = stim.Circuit.generated(
        "repetition_code:memory",
        distance=3,
        rounds=1,
    )

    dem = circuit.detector_error_model()
    print(f"Number of error instructions: {len(list(dem))}")
    print(f"\nFirst 10 error instructions:")
    for i, instruction in enumerate(dem):
        if i >= 10:
            break
        print(f"  {instruction}")


def main() -> None:
    repetition_code()
    detector_error_model()


if __name__ == "__main__":
    main()
