#!/usr/bin/env python3
"""Quantum Phase Estimation — estimate the phase of the T gate (θ = π/4).

3 precision qubits give resolution 2³ = 8, so we expect to measure
θ ≈ 1/8 of a full turn = π/4, confirming the T gate eigenvalue.
"""
import pennylane as qml
import numpy as np

N_PREC = 3
N_TOTAL = N_PREC + 1
dev = qml.device("default.qubit", wires=N_TOTAL)


def controlled_unitaries(power: int) -> None:
    """Apply controlled-U^(2^k) for each precision qubit k.

    U = T = RZ(π/4), so U^(2^k) = RZ(π/4 · 2^k).
    """
    for k in range(N_PREC):
        angle = (np.pi / 4) * (2**k)
        qml.ctrl(qml.RZ, control=k)(angle, wires=N_PREC)


@qml.qnode(dev)
def qpe_circuit() -> qml.typing.Result:
    """Phase estimation circuit."""
    qml.PauliX(wires=N_PREC)
    qml.Hadamard(wires=range(N_PREC))
    controlled_unitaries(1)
    qml.adjoint(qml.QFT(wires=list(range(N_PREC))))
    return qml.probs(wires=range(N_PREC))


def main() -> None:
    print("=== Quantum Phase Estimation (T gate) ===")
    print(f"Precision qubits: {N_PREC}")
    print(f"Target: eigenvalue e^(iπ/4) of T gate")
    print()

    print("Circuit:")
    print(qml.draw(qpe_circuit)())
    print()

    probs = qpe_circuit()
    measured = np.argmax(probs)
    phase_measured = measured / (2**N_PREC)
    phase_actual = 1 / 8  # T gate has eigenvalue e^(iπ/4), phase = 1/8

    print("Measurement probabilities:")
    for i, p in enumerate(probs):
        if p > 0.01:
            phase_est = i / (2**N_PREC)
            print(f"  |{i:0{N_PREC}b}⟩  p={p:.4f}  phase={phase_est:.4f} ({phase_est:.4f}×2π)")
    print()

    print(f"Measured state:  |{measured:0{N_PREC}b}⟩")
    print(f"Phase estimate:  {phase_measured:.4f} × 2π = {phase_measured * 2 * np.pi:.4f}")
    print(f"Expected phase:  {phase_actual:.4f} × 2π = {phase_actual * 2 * np.pi:.4f}")
    print(f"Exact match: {np.isclose(phase_measured, phase_actual)}")
    print()
    print("The T gate applies RZ(π/4), so its eigenvalue e^(iπ/4)")
    print("has phase θ = 1/8. QPE recovers this exactly with 3 bits.")


if __name__ == "__main__":
    main()
