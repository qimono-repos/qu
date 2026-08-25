import Std.Intrinsic.*;
import Std.Diagnostics.*;

@EntryPoint()
operation Statevectors() : Unit {
    Message("=== Statevector Inspection ===");

    // |0⟩ — default state
    use q = Qubit();
    Message("Initial state |0⟩:");
    DumpMachine();
    Reset(q);

    // |1⟩ — after X
    use q1 = Qubit();
    X(q1);
    Message("After X → |1⟩:");
    DumpMachine();
    Reset(q1);

    // |+⟩ — after H
    use q2 = Qubit();
    H(q2);
    Message("After H → |+⟩ = (|0⟩ + |1⟩)/√2:");
    DumpMachine();
    Reset(q2);

    // |−⟩ — after X then H
    use q3 = Qubit();
    X(q3);
    H(q3);
    Message("After X,H → |−⟩ = (|0⟩ − |1⟩)/√2:");
    DumpMachine();
    Reset(q3);
}
