import Std.Intrinsic.*;
import Std.Measurement.*;

operation OracleConstant0(inputs : Q[], target : Q) : Unit {}

operation OracleConstant1(inputs : Q[], target : Q) : Unit {
    X(target);
}

operation OracleBalanced(inputs : Q[], target : Q) : Unit {
    CNOT(inputs[0], target);
}

operation RunDJ(oracle : ((Q[], Q) => Unit)) : Result[] {
    use (q0, q1, target) = (Qubit(), Qubit(), Qubit());

    X(target);
    H(q0);
    H(q1);
    H(target);

    oracle([q0, q1], target);

    H(q0);
    H(q1);

    let r0 = M(q0);
    let r1 = M(q1);

    Reset(q0);
    Reset(q1);
    Reset(target);

    return [r0, r1];
}

@EntryPoint()
operation DeutschJozsa() : Unit {
    Message("=== Deutsch-Jozsa Algorithm (n=2) ===");

    Message("Testing constant-0 oracle:");
    let r0 = RunDJ(OracleConstant0);
    Message($"  Measured: ({r0[0]}, {r0[1]}) → Constant");

    Message("Testing constant-1 oracle:");
    let r1 = RunDJ(OracleConstant1);
    Message($"  Measured: ({r1[0]}, {r1[1]}) → Constant");

    Message("Testing balanced oracle:");
    let r2 = RunDJ(OracleBalanced);
    Message($"  Measured: ({r2[0]}, {r2[1]}) → Balanced");
}
