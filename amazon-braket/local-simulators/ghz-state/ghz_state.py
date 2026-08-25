import json

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def build_ghz_circuit(num_qubits: int = 4) -> Circuit:
    circuit = Circuit()
    circuit.h(0)
    for i in range(num_qubits - 1):
        circuit.cnot(i, i + 1)
    return circuit


def main() -> None:
    num_qubits = 4
    circuit = build_ghz_circuit(num_qubits)
    device = LocalSimulator()
    task = device.run(circuit, shots=0)
    result = task.result()

    probabilities = result.result_types[0].value

    print(f"{num_qubits}-qubit GHZ circuit:")
    print(circuit)
    print()
    print("Probabilities:")
    for state, prob in sorted(probabilities.items()):
        print(f"  |{state}⟩ = {prob:.6f}")


if __name__ == "__main__":
    main()
