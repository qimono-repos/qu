import cudaq
import numpy as np


@cudaq.kernel
def bell_state():
    qubits = cudaq.qvector(2)
    h(qubits[0])
    cx(qubits[0], qubits[1])


@cudaq.kernel
def ghz_state():
    qubits = cudaq.qvector(3)
    h(qubits[0])
    cx(qubits[0], qubits[1])
    cx(qubits[1], qubits[2])


if __name__ == "__main__":
    print("=== Bell state |Phi+> ===")
    result = cudaq.sample(bell_state, shots_count=1000)
    sv = np.array(cudaq.get_state(bell_state))
    probs = np.abs(sv) ** 2
    print(f"Statevector: |00>={sv[0]:.4f}  |01>={sv[1]:.4f}  "
          f"|10>={sv[2]:.4f}  |11>={sv[3]:.4f}")
    print(f"Probabilities: |00>={probs[0]:.4f}  |01>={probs[1]:.4f}  "
          f"|10>={probs[2]:.4f}  |11>={probs[3]:.4f}")
    print("Measured correlations:")
    for bitstring, count in result.items():
        print(f"  |{bitstring}>: {count}")
    print("(Only |00> and |11> — qubits are perfectly correlated)")

    print("\n=== 3-qubit GHZ state ===")
    result2 = cudaq.sample(ghz_state, shots_count=1000)
    sv2 = np.array(cudaq.get_state(ghz_state))
    probs2 = np.abs(sv2) ** 2
    basis = ["|000>", "|001>", "|010>", "|011>",
             "|100>", "|101>", "|110>", "|111>"]
    print("Statevector amplitudes:")
    for b, amp, prob in zip(basis, sv2, probs2):
        if abs(prob) > 0.001:
            print(f"  {b}: {amp:.4f} (P={prob:.4f})")
    print("Measured:")
    for bitstring, count in result2.items():
        print(f"  |{bitstring}>: {count}")
