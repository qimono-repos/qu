import numpy as np

try:
    from bloqade.squin import kernel, measure, assigned_variable

    SQUIN_AVAILABLE = True
except ImportError:
    SQUIN_AVAILABLE = False

if not SQUIN_AVAILABLE:
    import cirq
    from bloqade.circuit import load_circuit


def ghz_squin() -> None:
    n_qubits = 4

    @kernel
    def prepare_ghz():
        qubits = [0, 1, 2, 3]
        h(qubits[0])
        for i in range(n_qubits - 1):
            cx(qubits[i], qubits[i + 1])
        for i in range(n_qubits):
            m = measure(qubits[i])
            if m == 1:
                x(qubits[i])

    prepare_ghz()
    print("GHZ state prepared via SQUIN (4 qubits)")
    print("Mid-circuit measurement + feed-forward applied")


def ghz_cirq_fallback() -> None:
    q = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append([cirq.CNOT(q[i], q[i + 1]) for i in range(3)])
    circuit.append([cirq.measure(q[i], key=str(i)) for i in range(4)])

    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=10)
    print("GHZ state via Cirq (fallback, 4 qubits):")
    print(result)


def main() -> None:
    if SQUIN_AVAILABLE:
        ghz_squin()
    else:
        print("SQUIN not available, falling back to Cirq interop")
        ghz_cirq_fallback()


if __name__ == "__main__":
    main()
