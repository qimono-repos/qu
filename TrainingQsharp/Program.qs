namespace TrainingQsharp {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Diagnostics;

    @EntryPoint()
    operation HelloQuantumWorld() : (Result, Result) {
        // let max = 100;
        // Message($"Generating a random number between 0 and {max}: ");
        // return GenerateRandomNumberInRange(max);
        return GenerateAndMeasureBellState();
    }
}
