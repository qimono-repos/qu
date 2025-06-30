/// # Quantum Hello to Qimono!
///
/// This Q# code generates a random bit by setting a qubit in a superposition of
/// the computational basis states |0〉 and |1〉, and returning the measurement result.
namespace QuantumHelloWorld {

    @EntryPoint()
    operation RandomBit() : Result {
        Message("Say Hello to Qimono !!!");
        use qubit_001 = Qubit();
        use qubit_002 = Qubit();
        // Set the qubit in superposition by applying a Hadamard transformation.
        H(qubit_001);
        CNOT(qubit_001, qubit_002);

        // Measure the qubit. There is a 50% probability of measuring either 'Zero' or 'One'.
        let result = M(qubit_001);

        // Reset the qubit so it can be safely released.
        Reset(qubit_001);
        Reset(qubit_002);
        return result;
    }
}