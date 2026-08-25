"""Noise models and threshold behavior in quantum error correction.

Compares logical vs physical error rates across different code distances.
"""

import stim
import numpy as np


def depolarizing_noise() -> None:
    """Compare logical error rates with depolarizing noise."""
    print("=== Depolarizing Noise: Logical vs Physical Error Rates ===\n")

    physical_error_rates = [0.001, 0.005, 0.01, 0.02, 0.05]
    distances = [3, 5, 7]
    num_shots = 5000

    for p in physical_error_rates:
        print(f"\nPhysical error rate p = {p}:")
        for d in distances:
            circuit = stim.Circuit.generated(
                "repetition_code:memory",
                distance=d,
                rounds=1,
                after_clifford_depolarization=p,
                before_round_data_depolarization=p,
            )

            sampler = circuit.compile_detector_error_model()
            detection_events = sampler.sample(num_shots)

            # Count logical errors (any detection event triggered)
            has_error = np.any(detection_events, axis=1)
            logical_error_rate = np.mean(has_error)

            print(f"  Distance {d}: logical error rate = {logical_error_rate:.4f} "
                  f"({np.sum(has_error)}/{num_shots})")


def bit_flip_vs_phase_flip() -> None:
    """Compare bit-flip and phase-flip noise models."""
    print("\n=== Bit-Flip vs Phase-Flip Noise ===\n")

    error_rate = 0.02
    num_shots = 5000

    # Bit-flip noise
    bit_circuit = stim.Circuit(f"""
        H 0
        H 1
        H 2
        X_ERROR({error_rate}) 0 1 2
        H 0
        H 1
        H 2
        M 0 1 2
    """)

    sampler = bit_circuit.compile_sampler()
    bit_results = sampler.sample(num_shots)

    # Count bit-flip errors
    bit_errors = np.sum(np.any(bit_results != bit_results[0], axis=1))
    print(f"Bit-flip noise (p={error_rate}):")
    print(f"  Errors detected: {bit_errors}/{num_shots} ({100*bit_errors/num_shots:.1f}%)")

    # Phase-flip noise
    phase_circuit = stim.Circuit(f"""
        Z_ERROR({error_rate}) 0 1 2
        M 0 1 2
    """)

    sampler = phase_circuit.compile_sampler()
    phase_results = sampler.sample(num_shots)

    phase_errors = np.sum(np.any(phase_results != phase_results[0], axis=1))
    print(f"\nPhase-flip noise (p={error_rate}):")
    print(f"  Errors detected: {phase_errors}/{num_shots} ({100*phase_errors/num_shots:.1f}%)")


def main() -> None:
    depolarizing_noise()
    bit_flip_vs_phase_flip()


if __name__ == "__main__":
    main()
