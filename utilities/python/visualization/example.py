"""Example: save a Bell state circuit, Bloch sphere, and distribution."""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from visualization import save_bloch, save_circuit, save_distribution


def main() -> None:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)

    save_circuit(qc, "bell_circuit")
    save_bloch(qc, "bell_bloch")

    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities_dict()
    save_distribution(probs, "bell_distribution")


if __name__ == "__main__":
    main()
