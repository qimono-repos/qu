import Std.Intrinsic.*;
import Std.Measurement.*;

@EntryPoint()
operation OracleBasics() : Unit {
    Message("=== Oracle Basics: Marking |11⟩ ===");

    use (q0, q1, target) = (Qubit(), Qubit(), Qubit());

    H(q0);
    H(q1);
    X(target);
    H(target);

    Controlled X([q0, q1], target);

    H(target);
    X(target);

    let r0 = M(q0);
    let r1 = M(q1);
    Message($"Measured: q0={r0}, q1={r1}");

    Reset(q0);
    Reset(q1);
    Reset(target);
}
