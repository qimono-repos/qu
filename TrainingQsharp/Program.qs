namespace TrainingQsharp {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Diagnostics;

    @EntryPoint()
    operation HelloQuantumWorld() : Result[] 
    //(Result, Result) 
    {
        // let max = 100;
        // Message($"Generating a random number between 0 and {max}: ");
        // return GenerateRandomNumberInRange(max);
        
        //return GenerateAndMeasureBellState();

            // Allocate the message and bob qubits
    use (message, bob) = (Qubit(), Qubit());

    // Use the `Teleport` operation to send different quantum states
    let stateInitializerBasisTuples = [
        ("|0〉", I, PauliZ),
        ("|1〉", X, PauliZ),
        ("|+〉", SetToPlus, PauliX),
        ("|-〉", SetToMinus, PauliX)
    ];

    mutable results = [];
    for (state, initializer, basis) in stateInitializerBasisTuples {
        // Initialize the message and show its state using the `DumpMachine`
        // function.
        initializer(message);
        Message($"Teleporting state {state}");
        DumpMachine();

        // Teleport the message and show the quantum state after
        // teleportation.
        Teleport(message, bob);
        Message($"Received state {state}");
        DumpMachine();

        // Measure bob in the corresponding basis and reset the qubits to
        // continue teleporting more messages.
        let result = Measure([basis], [bob]);
        set results += [result];
        ResetAll([message, bob]);
    }

    return results;
    }
}
