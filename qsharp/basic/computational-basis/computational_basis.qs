import Std.Intrinsic.*;
import Std.Measurement.*;

@EntryPoint()
operation ComputationalBasis() : Unit {
    Message("=== Computational Basis States ===");

    // Prepare |0⟩ (default state) and measure
    use q0 = Qubit();
    let r0 = M(q0);
    Message($"|0⟩ measured: {r0}");
    Reset(q0);

    // Prepare |1⟩ via X gate and measure
    use q1 = Qubit();
    X(q1);
    let r1 = M(q1);
    Message($"|1⟩ measured: {r1}");
    Reset(q1);
}
