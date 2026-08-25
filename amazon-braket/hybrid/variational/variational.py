import numpy as np
from braket.circuit import Circuit, Parameter
from braket.devices import LocalSimulator
from braket.parametric import FreeParameter


def build_variational_circuit(params: list[float]) -> Circuit:
    circuit = Circuit()
    circuit.rx(0, params[0])
    circuit.ry(0, params[1])
    circuit.rx(1, params[2])
    circuit.ry(1, params[3])
    circuit.cnot(0, 1)
    circuit.rz(1, params[4])
    circuit.cnot(0, 1)
    return circuit


def compute_energy(statevector: np.ndarray) -> float:
    z0z1 = np.array([
        [1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, 1],
    ])
    z0 = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ])
    z1 = np.array([
        [1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1],
    ])
    hamiltonian = 0.5 * np.kron(np.eye(2), np.eye(2)) - 0.8 * z0z1 + 0.3 * z0 - 0.2 * z1
    sv = statevector.reshape(-1, 1)
    energy = float(np.real(sv.conj().T @ hamiltonian @ sv))
    return energy


def main() -> None:
    device = LocalSimulator()
    rng = np.random.default_rng(42)
    params = rng.uniform(0, 2 * np.pi, size=5).tolist()
    lr = 0.1

    print("VQE-style optimization loop (2-qubit Hamiltonian)")
    print("=" * 50)

    for step in range(20):
        circuit = build_variational_circuit(params)
        task = device.run(circuit, shots=0)
        result = task.result()
        sv = np.array(result.result_types[0].value, dtype=complex)

        energy = compute_energy(sv)

        gradients = np.zeros(5)
        for i in range(5):
            params_plus = params.copy()
            params_plus[i] += np.pi / 2
            params_minus = params.copy()
            params_minus[i] -= np.pi / 2

            task_plus = device.run(build_variational_circuit(params_plus), shots=0)
            sv_plus = np.array(task_plus.result().result_types[0].value, dtype=complex)
            e_plus = compute_energy(sv_plus)

            task_minus = device.run(build_variational_circuit(params_minus), shots=0)
            sv_minus = np.array(task_minus.result().result_types[0].value, dtype=complex)
            e_minus = compute_energy(sv_minus)

            gradients[i] = (e_plus - e_minus) / 2.0

        params = [p - lr * g for p, g in zip(params, gradients)]

        if step % 5 == 0 or step == 19:
            print(f"  step {step:>2d}  energy = {energy:.6f}  params = [{', '.join(f'{p:.4f}' for p in params)}]")

    print()
    print(f"Final energy: {energy:.6f}")
    print("Exact ground state energy for this Hamiltonian ≈ -1.0607")


if __name__ == "__main__":
    main()
