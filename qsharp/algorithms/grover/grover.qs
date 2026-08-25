import Std.Intrinsic.*;
import Std.Measurement.*;

operation Oracle(qubits : Qubit[], target : Qubit) : Unit {
    Controlled X(qubits, target);
}

operation GroverDiffusion(qubits : Qubit[]) : Unit {
    for q in qubits {
        H(q);
    }
    for q in qubits {
        X(q);
    }

    Controlled Z([qubits[0]], qubits[1]);
    Controlled Z([qubits[0], qubits[1]], qubits[2]);

    for q in qubits {
        X(q);
    }
    for q in qubits {
        H(q);
    }
}

@EntryPoint()
operation Grover() : Unit {
    Message("=== Grover Search (3 qubits, target |111⟩) ===");

    use qubits = Qubit[3];
    use target = Qubit();

    for q in qubits {
        H(q);
    }
    H(target);
    X(target);

    let iterations = 2;

    for _ in 1..iterations {
        Oracle(qubits, target);
        GroverDiffusion(qubits);
    }

    let r0 = M(qubits[0]);
    let r1 = M(qubits[1]);
    let r2 = M(qubits[2]);
    Message($"Measured: {r2}{r1}{r0}");

    ResetAll(qubits);
    Reset(target);
}
