import json

from braket.circuit import Circuit
from braket.devices import LocalSimulator


def build_bell_circuit() -> Circuit:
    circuit = Circuit()
    circuit.h(0)
    circuit.cnot(0, 1)
    return circuit


def main() -> None:
    circuit = build_bell_circuit()
    device = LocalSimulator()
    task = device.run(circuit, shots=0)
    result = task.result()

    state_vector = result.result_types[0].value
    probabilities = result.result_types[1].value

    print("Bell state circuit:")
    print(circuit)
    print()
    print(f"State vector: {state_vector}")
    print(f"Probabilities: {json.dumps({k: round(v, 6) for k, v in probabilities.items()})}")


if __name__ == "__main__":
    main()
