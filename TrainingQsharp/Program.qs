namespace TrainingQsharp {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Diagnostics;

    @EntryPoint()
    operation HelloQuantumWorld() : Result {
        Message("-  ");
        Message("-  ");
        Message("-  ");
        Message("-  ");
        Message("-  ");
        Message("-  ");
        Message("-  ");
        Message("-  ");
        Message("-  ");
        Message("-  ");
        Message("-  ");
        Message("-  ");
        use q = Qubit();
        H(q);
        let result = M(q);
        Reset(q);
        Message("Hello quantum world!!!!");
        return result;
    }
}

