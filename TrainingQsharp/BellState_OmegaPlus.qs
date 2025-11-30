namespace TrainingQsharp.RandomUtils {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Diagnostics;  // Aka Std.Diagnostics.*;

    operation GenerateEntanglement() : (Result, Result) {
        use (q1,q2) = (Qubit(), Qubit());

        H(q1);
        CNOT(q1,q2);

        Message("Entanglement generated.");

        DumpMachine();

        let (m1, m2) = (M(q1), M(q2));

        // let result = (M(q1), M(q2));
        Reset(q1);
        Reset(q2);

        return (m1, m2);
    }

}