import Std.Intrinsic.*;
import Std.Diagnostics.*;

@EntryPoint()
operation LogicGates() : Unit {
    Message("=== Single-Qubit Logic Gates ===");

    // X gate (NOT)
    use q = Qubit();
    X(q);
    Message("After X (bit-flip):");
    DumpMachine();
    Reset(q);

    // Y gate
    use q2 = Qubit();
    Y(q2);
    Message("After Y:");
    DumpMachine();
    Reset(q2);

    // Z gate
    use q3 = Qubit();
    X(q3);
    Z(q3);
    Message("After X then Z (phase-flip on |1⟩):");
    DumpMachine();
    Reset(q3);

    // H gate (Hadamard)
    use q4 = Qubit();
    H(q4);
    Message("After H → |+⟩:");
    DumpMachine();
    Reset(q4);

    // S gate (√Z)
    use q5 = Qubit();
    H(q5);
    S(q5);
    Message("After H then S:");
    DumpMachine();
    Reset(q5);

    // T gate (√S)
    use q6 = Qubit();
    H(q6);
    T(q6);
    Message("After H then T:");
    DumpMachine();
    Reset(q6);
}
