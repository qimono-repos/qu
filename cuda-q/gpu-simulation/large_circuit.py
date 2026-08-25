import random
import time
import cudaq


@cudaq.kernel
def random_circuit(qubit_count: int, gates: list[int]):
    qubits = cudaq.qvector(qubit_count)
    for i in range(qubits.__len__()):
        gate_idx = gates[i] % 3
        if gate_idx == 0:
            h(qubits[i])
        elif gate_idx == 1:
            rx(float(i) * 0.5, qubits[i])
        else:
            ry(float(i) * 0.3, qubits[i])
    for i in range(qubits.__len__() - 1):
        cx(qubits[i], qubits[i + 1])


if __name__ == "__main__":
    n_qubits = 20
    n_shots = 1000
    gates = [random.randint(0, 100) for _ in range(n_qubits)]

    print(f"Simulating {n_qubits}-qubit random circuit with {n_shots} shots...")

    start = time.perf_counter()
    result = cudaq.sample(random_circuit, n_qubits, gates, shots_count=n_shots)
    elapsed = time.perf_counter() - start

    print(f"Simulation completed in {elapsed:.4f}s")
    print(f"Unique outcomes: {len(result)}")
    top = sorted(result.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Top 5 outcomes:")
    for bitstring, count in top:
        print(f"  |{bitstring}>: {count}")
