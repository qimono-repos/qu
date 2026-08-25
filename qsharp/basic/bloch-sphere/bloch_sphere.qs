import Std.Intrinsic.*;
import Std.Diagnostics.*;

@EntryPoint()
operation BlochSphere() : Unit {
    Message("=== Bloch Sphere: Single-Qubit Rotations ===");

    // Rx(π/2) rotation
    use q = Qubit();
    Rx(PI() / 2.0, q);
    Message("After Rx(π/2):");
    DumpMachine();
    Reset(q);

    // Ry(π/2) rotation
    use q2 = Qubit();
    Ry(PI() / 2.0, q2);
    Message("After Ry(π/2):");
    DumpMachine();
    Reset(q2);

    // Rz(π/2) rotation — needs superposition first to see effect
    use q3 = Qubit();
    H(q3);
    Rz(PI() / 2.0, q3);
    Message("After H then Rz(π/2):");
    DumpMachine();
    Reset(q3);

    // Full rotation back to |0⟩
    use q4 = Qubit();
    Rx(PI(), q4);
    Message("After Rx(π) (|0⟩ → |1⟩):");
    DumpMachine();
    Reset(q4);
}
