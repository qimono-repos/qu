namespace TrainingQsharp {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;

    operation MeasureOneQubit() : Result {
        use q = Qubit();
        let r = M(q);
        Reset(q);
        Message($"MeasureOneQubit measured: {r}");
        return r;
    }
}
