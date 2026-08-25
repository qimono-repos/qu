namespace TrainingQsharp {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Measurement;

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

    operation Teleport(message : Qubit, bob : Qubit) : Unit {
        // Allocate an alice qubit.
        use alice = Qubit();

        // Create some entanglement that we can use to send our message
        H(alice);
        CNOT(alice, bob);

        // Encode the message into the entangled pair
        CNOT(message, alice);

        // Transform the Bell states into computational states for measurement
        H(message);

        // Measure the qubits to extract the classical data we need to decode
        // the message by applying the corrections on the bob qubit
        // accordingly.
        if M(message) == One {
            Z(bob);
        }
        if M(alice) == One {
            X(bob);
        }

        // Reset alice qubit before releasing
        Reset(alice);
    }

    /// Sets a qubit in state |0⟩ to |+⟩.
    operation SetToPlus(q : Qubit) : Unit is Adj + Ctl {
        H(q);
    }

    /// Sets a qubit in state |0⟩ to |−⟩.
    operation SetToMinus(q : Qubit) : Unit is Adj + Ctl {
        X(q);
        H(q);
    }
}