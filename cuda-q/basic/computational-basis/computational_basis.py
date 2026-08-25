import cudaq


@cudaq.kernel
def zero_state():
    qubit = cudaq.qvector(1)


@cudaq.kernel
def one_state():
    qubit = cudaq.qvector(1)
    x(qubit[0])


if __name__ == "__main__":
    print("=== |0> state ===")
    result_zero = cudaq.sample(zero_state, shots_count=1000)
    for bitstring, count in result_zero.items():
        print(f"  |{bitstring}>: {count}")

    print("\n=== |1> state ===")
    result_one = cudaq.sample(one_state, shots_count=1000)
    for bitstring, count in result_one.items():
        print(f"  |{bitstring}>: {count}")
