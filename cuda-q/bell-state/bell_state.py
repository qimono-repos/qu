import cudaq


@cudaq.kernel
def bell():
    qubits = cudaq.qvector(2)
    h(qubits[0])
    cx(qubits[0], qubits[1])


if __name__ == "__main__":
    result = cudaq.sample(bell, shots_count=1000)
    print("Bell state results:")
    for bitstring, count in result.items():
        print(f"  |{bitstring}>: {count}")
