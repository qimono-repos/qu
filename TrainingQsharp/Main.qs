namespace TrainingQsharp {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Canon;

    operation MainMeasure() : Result {
        use q = Qubit();
        let r = M(q);
        Reset(q);
        Message($"Main measured: {r}");
        return r;
    }
}
