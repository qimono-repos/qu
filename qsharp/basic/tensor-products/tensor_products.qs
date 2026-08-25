import Std.Intrinsic.*;
import Std.Diagnostics.*;

@EntryPoint()
operation TensorProducts() : Unit {
    Message("=== Tensor Products: Two-Qubit Systems ===");

    // |00⟩ — default
    use (q1, q2) = (Qubit(), Qubit());
    Message("Initial |00⟩:");
    DumpMachine();
    Reset(q1);
    Reset(q2);

    // |01⟩
    use (q3, q4) = (Qubit(), Qubit());
    X(q4);
    Message("After X on q1 → |01⟩:");
    DumpMachine();
    Reset(q3);
    Reset(q4);

    // |10⟩
    use (q5, q6) = (Qubit(), Qubit());
    X(q5);
    Message("After X on q0 → |10⟩:");
    DumpMachine();
    Reset(q5);
    Reset(q6);

    // |11⟩
    use (q7, q8) = (Qubit(), Qubit());
    X(q7);
    X(q8);
    Message("After X on both → |11⟩:");
    DumpMachine();
    Reset(q7);
    Reset(q8);

    // |+0⟩ = H⊗I |00⟩
    use (q9, q10) = (Qubit(), Qubit());
    H(q9);
    Message("After H on q0 → |+0⟩:");
    DumpMachine();
    Reset(q9);
    Reset(q10);
}
