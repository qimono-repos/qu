import Std.Intrinsic.*;
import Std.Measurement.*;

operation ApplyModularAddition(a : Int, controls : Qubit[], target : Qubit) : Unit {
    for ctrl in controls {
        Controlled X([ctrl], target);
    }
}

@EntryPoint()
operation Shor() : Unit {
    Message("=== Shor's Algorithm (Simplified Factoring of 15) ===");
    Message("Target: N = 15");
    Message("Chosen: a = 7");
    Message("");

    let a = 7;
    let N = 15;
    let n = 4;

    use control = Qubit[n];
    use target = Qubit();

    H(control[0]);
    X(target);

    for i in 0..n - 1 {
        let power = 1 <<< i;
        for _ in 1..power {
            Controlled ApplyModularAddition([control[i]], (a, [control[i]], target));
        }
    }

    for i in 0..n / 2 - 1 {
        Swap(control[i], control[n - 1 - i]);
    }

    let result = MeasureInteger(control);
    Message($"Measured: {result}");
    Message("");
    Message("Classical post-processing would find:");
    Message("  gcd(a^(r/2) + 1, N) and gcd(a^(r/2) - 1, N)");
    Message("  where r is the period from phase estimation");
    Message("  For a=7, N=15: factors are 3 and 5");

    ResetAll(control);
    Reset(target);
}
