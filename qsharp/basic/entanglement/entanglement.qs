import Std.Intrinsic.*;
import Std.Measurement.*;
import Std.Diagnostics.*;

@EntryPoint()
operation Entanglement() : Unit {
    Message("=== Bell State Entanglement ===");

    // Create |Φ+⟩ = (|00⟩ + |11⟩)/√2
    use (q1, q2) = (Qubit(), Qubit());
    H(q1);
    CNOT(q1, q2);
    Message("Bell state |Φ+⟩ created:");
    DumpMachine();

    let r1 = M(q1);
    let r2 = M(q2);
    Message($"Measured: ({r1}, {r2})");
    Message("Both qubits always agree — that is entanglement!");
    Reset(q1);
    Reset(q2);

    // Create |Φ−⟩ = (|00⟩ − |11⟩)/√2
    Message("");
    Message("Bell state |Φ−⟩:");
    use (q3, q4) = (Qubit(), Qubit());
    H(q3);
    CNOT(q3, q4);
    Z(q3);
    Message("After H, CNOT, Z on q0:");
    DumpMachine();
    let r3 = M(q3);
    let r4 = M(q4);
    Message($"Measured: ({r3}, {r4})");
    Reset(q3);
    Reset(q4);

    // Create |Ψ+⟩ = (|01⟩ + |10⟩)/√2
    Message("");
    Message("Bell state |Ψ+⟩:");
    use (q5, q6) = (Qubit(), Qubit());
    H(q5);
    CNOT(q5, q6);
    X(q6);
    Message("After H, CNOT, X on q1:");
    DumpMachine();
    let r5 = M(q5);
    let r6 = M(q6);
    Message($"Measured: ({r5}, {r6})");
    Reset(q5);
    Reset(q6);
}
