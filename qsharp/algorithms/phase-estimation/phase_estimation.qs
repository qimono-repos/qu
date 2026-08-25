import Std.Intrinsic.*;
import Std.Math.*;
import Std.Measurement.*;

operation ApplyTPower(power : Int, target : Qubit) : Unit {
    for _ in 1..power {
        T(target);
    }
}

@EntryPoint()
operation PhaseEstimation() : Unit {
    Message("=== Quantum Phase Estimation (T gate) ===");

    use precision = Qubit[3];
    use target = Qubit();

    X(target);

    for q in precision {
        H(q);
    }

    ApplyTPower(4, target);
    Controlled ApplyTPower([precision[2]], (4, target));

    ApplyTPower(2, target);
    Controlled ApplyTPower([precision[1]], (2, target));

    ApplyTPower(1, target);
    Controlled ApplyTPower([precision[0]], (1, target));

    for i in 0..1 {
        Swap(precision[i], precision[2 - i]);
    }

    let result = MeasureInteger(precision);
    let phase = IntAsDouble(result) / IntAsDouble(1 <<< 3);
    Message($"Estimated phase: {phase} (1/8 increments)");
    Message("T gate phase = 1/8 = 0.125");

    ResetAll(precision);
    Reset(target);
}
