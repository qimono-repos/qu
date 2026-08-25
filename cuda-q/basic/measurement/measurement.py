import cudaq
import numpy as np


@cudaq.kernel
def plus_state():
    qubit = cudaq.qvector(1)
    h(qubit[0])


@cudaq.kernel
def minus_state():
    qubit = cudaq.qvector(1)
    x(qubit[0])
    h(qubit[0])


@cudaq.kernel
def ibasis_state():
    qubit = cudaq.qvector(1)
    h(qubit[0])
    s(qubit[0])


if __name__ == "__main__":
    print("=== |+> state (equal superposition) ===")
    result = cudaq.sample(plus_state, shots_count=1000)
    for bitstring, count in result.items():
        print(f"  |{bitstring}>: {count}")

    sv = cudaq.get_state(plus_state)
    amps = np.array(sv)
    print(f"Statevector: |0>={amps[0]:.4f}  |1>={amps[1]:.4f}")

    print("\n=== |-> state (phase-flipped superposition) ===")
    result2 = cudaq.sample(minus_state, shots_count=1000)
    for bitstring, count in result2.items():
        print(f"  |{bitstring}>: {count}")

    sv2 = cudaq.get_state(minus_state)
    amps2 = np.array(sv2)
    print(f"Statevector: |0>={amps2[0]:.4f}  |1>={amps2[1]:.4f}")

    print("\n=== |i> state (circular basis) ===")
    result3 = cudaq.sample(ibasis_state, shots_count=1000)
    for bitstring, count in result3.items():
        print(f"  |{bitstring}>: {count}")

    sv3 = cudaq.get_state(ibasis_state)
    amps3 = np.array(sv3)
    print(f"Statevector: |0>={amps3[0]:.4f}  |1>={amps3[1]:.4f}")
