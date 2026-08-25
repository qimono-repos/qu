import Std.Intrinsic.*;
import Std.Diagnostics.*;

@EntryPoint()
operation Phase() : Unit {
    Message("=== Phase Gates: S and T ===");

    // S gate adds a phase of i to |1⟩
    use q = Qubit();
    H(q);
    Message("After H (equal superposition):");
    DumpMachine();
    S(q);
    Message("After S (phase = +i/2 on |1⟩ component):");
    DumpMachine();
    Reset(q);

    // T gate adds a phase of e^{iπ/4} to |1⟩
    use q2 = Qubit();
    H(q2);
    T(q2);
    Message("After H then T (phase = +π/4 on |1⟩ component):");
    DumpMachine();
    Reset(q2);

    // S† (adjoint of S)
    use q3 = Qubit();
    H(q3);
    S(q3);
    Adjoint S(q3);
    Message("After H, S, S† (back to equal superposition):");
    DumpMachine();
    Reset(q3);

    // T† (adjoint of T)
    use q4 = Qubit();
    H(q4);
    T(q4);
    Adjoint T(q4);
    Message("After H, T, T† (back to equal superposition):");
    DumpMachine();
    Reset(q4);
}
