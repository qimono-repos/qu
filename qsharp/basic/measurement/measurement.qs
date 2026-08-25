import Std.Intrinsic.*;
import Std.Measurement.*;

@EntryPoint()
operation Measurement() : Unit {
    Message("=== Measurement in Z and X Bases ===");

    // Z-basis: measure directly
    Message("--- Z-basis measurement on |+⟩ ---");
    for i in 1 .. 5 {
        use q = Qubit();
        H(q);
        let result = M(q);
        Message($"  Round {i}: {result}");
        Reset(q);
    }

    // X-basis: apply H before measurement
    Message("--- X-basis measurement on |+⟩ ---");
    for i in 1 .. 5 {
        use q = Qubit();
        H(q);
        // Rotate into X basis: H flips Z↔X
        H(q);
        let result = M(q);
        Message($"  Round {i}: {result}");
        Reset(q);
    }

    // X-basis on |0⟩
    Message("--- X-basis measurement on |0⟩ ---");
    for i in 1 .. 5 {
        use q = Qubit();
        H(q);
        let result = M(q);
        Message($"  Round {i}: {result}");
        Reset(q);
    }
}
