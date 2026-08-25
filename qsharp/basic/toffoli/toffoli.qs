import Std.Intrinsic.*;
import Std.Measurement.*;

@EntryPoint()
operation Toffoli() : Unit {
    Message("=== Toffoli (CCX) Gate on 3 Qubits ===");

    // CCX with control=|00⟩: target unchanged
    Message("--- CCX (ctrl1=|0⟩, ctrl2=|0⟩) → target stays |0⟩ ---");
    use (c1, c2, tgt) = (Qubit(), Qubit(), Qubit());
    CCNOT(c1, c2, tgt);
    let r = M(tgt);
    Message($"  Target: {r}");
    Reset(c1);
    Reset(c2);
    Reset(tgt);

    // CCX with one control=|1⟩
    Message("--- CCX (ctrl1=|1⟩, ctrl2=|0⟩) → target stays |0⟩ ---");
    use (c3, c4, tgt2) = (Qubit(), Qubit(), Qubit());
    X(c3);
    CCNOT(c3, c4, tgt2);
    let r2 = M(tgt2);
    Message($"  Target: {r2}");
    Reset(c3);
    Reset(c4);
    Reset(tgt2);

    // CCX with both controls=|1⟩: target flips
    Message("--- CCX (ctrl1=|1⟩, ctrl2=|1⟩) → target flips to |1⟩ ---");
    use (c5, c6, tgt3) = (Qubit(), Qubit(), Qubit());
    X(c5);
    X(c6);
    CCNOT(c5, c6, tgt3);
    let r3 = M(tgt3);
    Message($"  Target: {r3}");
    Reset(c5);
    Reset(c6);
    Reset(tgt3);

    // Toffoli as AND gate demo
    Message("");
    Message("--- Toffoli as AND gate (full-adder carry) ---");
    use (a, b, carry) = (Qubit(), Qubit(), Qubit());
    X(a);
    X(b);
    CCNOT(a, b, carry);
    let ra = M(a);
    let rb = M(b);
    let rc = M(carry);
    Message($"  a=1, b=1 → carry={rc}");
    Reset(a);
    Reset(b);
    Reset(carry);
}
