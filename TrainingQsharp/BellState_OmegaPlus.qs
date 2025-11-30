namespace TrainingQsharp {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Diagnostics;

    operation GenerateAndMeasureBellState() : (Result, Result) {
        use (q1, q2) = (Qubit(), Qubit());

        H(q1);
        CNOT(q1, q2);

        Message("Entanglement generated. The state is now a Bell state |Φ+⟩.");

        DumpMachine();

        let (m1, m2) = (M(q1), M(q2));

        Reset(q1);
        Reset(q2);

        return (m1, m2);
    }

}