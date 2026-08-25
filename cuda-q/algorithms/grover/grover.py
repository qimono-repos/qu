import cudaq
import numpy as np


@cudaq.kernel
def grover_101():
    """Grover search for |101> in 3 qubits (N=8).
    
    1 Grover iteration: oracle marks |101>, diffusion amplifies.
    """
    qubits = cudaq.qvector(3)
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    x(qubits[0])
    x(qubits[2])
    cz(qubits[0], qubits[2])
    x(qubits[0])
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    x(qubits[0])
    x(qubits[1])
    x(qubits[2])
    cz(qubits[0], qubits[2])
    x(qubits[0])
    x(qubits[1])
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])


@cudaq.kernel
def grover_000():
    """Grover search for |000> in 3 qubits (N=8)."""
    qubits = cudaq.qvector(3)
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    cz(qubits[0], qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    x(qubits[0])
    x(qubits[1])
    x(qubits[2])
    cz(qubits[0], qubits[2])
    x(qubits[0])
    x(qubits[1])
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])


@cudaq.kernel
def grover_2iter():
    """Grover search for |101> with 2 iterations (optimal for N=8, 1 target)."""
    qubits = cudaq.qvector(3)
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    x(qubits[0])
    x(qubits[2])
    cz(qubits[0], qubits[2])
    x(qubits[0])
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    x(qubits[0])
    x(qubits[1])
    x(qubits[2])
    cz(qubits[0], qubits[2])
    x(qubits[0])
    x(qubits[1])
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    x(qubits[0])
    x(qubits[2])
    cz(qubits[0], qubits[2])
    x(qubits[0])
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])
    x(qubits[0])
    x(qubits[1])
    x(qubits[2])
    cz(qubits[0], qubits[2])
    x(qubits[0])
    x(qubits[1])
    x(qubits[2])
    h(qubits[0])
    h(qubits[1])
    h(qubits[2])


if __name__ == "__main__":
    print("=== Grover's search algorithm (3 qubits, N=8) ===\n")

    basis = ["|000>", "|001>", "|010>", "|011>",
             "|100>", "|101>", "|110>", "|111>"]

    print("--- Searching for |101> with 1 iteration ---")
    sv = np.array(cudaq.get_state(grover_101))
    probs = np.abs(sv) ** 2
    print("Amplitudes after 1 Grover iteration:")
    for b, amp, prob in zip(basis, sv, probs):
        print(f"  {b}: amp={amp:+.4f}  P={prob:.4f}")
    result = cudaq.sample(grover_101, shots_count=1000)
    for bitstring, count in result.items():
        print(f"  measured |{bitstring}>: {count}")

    print("\n--- Searching for |000> with 1 iteration ---")
    sv2 = np.array(cudaq.get_state(grover_000))
    probs2 = np.abs(sv2) ** 2
    print("Amplitudes after 1 Grover iteration:")
    for b, amp, prob in zip(basis, sv2, probs2):
        print(f"  {b}: amp={amp:+.4f}  P={prob:.4f}")
    result2 = cudaq.sample(grover_000, shots_count=1000)
    for bitstring, count in result2.items():
        print(f"  measured |{bitstring}>: {count}")

    print("\n--- Searching for |101> with 2 iterations (optimal) ---")
    sv3 = np.array(cudaq.get_state(grover_2iter))
    probs3 = np.abs(sv3) ** 2
    print("Amplitudes after 2 Grover iterations:")
    for b, amp, prob in zip(basis, sv3, probs3):
        print(f"  {b}: amp={amp:+.4f}  P={prob:.4f}")
    result3 = cudaq.sample(grover_2iter, shots_count=1000)
    for bitstring, count in result3.items():
        print(f"  measured |{bitstring}>: {count}")

    print("\n--- Optimal iteration count ---")
    N = 8
    optimal = int(np.round(np.pi / 4 * np.sqrt(N)))
    print(f"  N = {N}, optimal iterations = {optimal}")
    print(f"  Success probability ~ sin^2((2*{optimal}+1)*theta)")
    print(f"  where theta = arcsin(1/sqrt(N)) = "
          f"{np.degrees(np.arcsin(1/np.sqrt(N))):.1f} deg")

    print("\nGrover's algorithm provides quadratic speedup:")
    print(f"  Classical: O(N) = O({N}) queries")
    print(f"  Quantum:   O(sqrt(N)) = O({int(np.sqrt(N))}) queries")
