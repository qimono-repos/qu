import Std.Intrinsic.*;
import Std.Measurement.*;

@EntryPoint()
operation Superposition() : Unit {
    Message("=== Superposition: Hadamard + Repeated Measurement ===");
    Message("Measuring |+⟩ = H|0⟩ ten times:");

    mutable countZero = 0;
    mutable countOne = 0;

    for i in 1 .. 10 {
        use q = Qubit();
        H(q);
        let result = M(q);
        if result == Zero {
            set countZero += 1;
        } else {
            set countOne += 1;
        }
        Reset(q);
    }

    Message($"  |0⟩ outcomes: {countZero}");
    Message($"  |1⟩ outcomes: {countOne}");
    Message("Expected: roughly 50/50 split for a fair coin.");
}
