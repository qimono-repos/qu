import Std.Intrinsic.*;
import Std.Measurement.*;

@EntryPoint()
operation ControlledGates() : Unit {
    Message("=== Controlled Gates: CNOT and CZ ===");

    // CNOT with control=|0⟩: target unchanged
    Message("--- CNOT (control=|0⟩) → target stays |0⟩ ---");
    use (ctrl, tgt) = (Qubit(), Qubit());
    CNOT(ctrl, tgt);
    let r = M(tgt);
    Message($"  Target: {r}");
    Reset(ctrl);
    Reset(tgt);

    // CNOT with control=|1⟩: target flips
    Message("--- CNOT (control=|1⟩) → target flips to |1⟩ ---");
    use (ctrl2, tgt2) = (Qubit(), Qubit());
    X(ctrl2);
    CNOT(ctrl2, tgt2);
    let r2 = M(tgt2);
    Message($"  Target: {r2}");
    Reset(ctrl2);
    Reset(tgt2);

    // CZ: flips phase of |11⟩
    Message("--- CZ gate ---");
    use (ctrl3, tgt3) = (Qubit(), Qubit());
    X(ctrl3);
    X(tgt3);
    CZ(ctrl3, tgt3);
    let r3 = M(ctrl3);
    let r4 = M(tgt3);
    Message($"  |11⟩ after CZ: ({r3}, {r4})");
    Reset(ctrl3);
    Reset(tgt3);

    // Controlled-H
    Message("--- Controlled-H gate ---");
    use (ctrl4, tgt4) = (Qubit(), Qubit());
    X(ctrl4);
    CH(ctrl4, tgt4);
    Message("  After X(ctrl), CH(ctrl, tgt):");
    DumpMachine();
    Reset(ctrl4);
    Reset(tgt4);
}
