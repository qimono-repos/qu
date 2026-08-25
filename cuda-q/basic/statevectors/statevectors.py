import cudaq
import numpy as np


@cudaq.kernel
def plus_state():
    qubit = cudaq.qvector(1)
    h(qubit[0])


if __name__ == "__main__":
    print("=== |+> state vector ===")
    result = cudaq.sample(plus_state, shots_count=1000)
    for bitstring, count in result.items():
        print(f"  |{bitstring}>: {count}")

    sv = cudaq.get_state(plus_state)
    amplitudes = np.array(sv)
    print(f"\nAmplitudes: {amplitudes}")
    print(f"|0> amplitude: {amplitudes[0]:.4f}")
    print(f"|1> amplitude: {amplitudes[1]:.4f}")
    print(f"|0> probability: {abs(amplitudes[0])**2:.4f}")
    print(f"|1> probability: {abs(amplitudes[1])**2:.4f}")
