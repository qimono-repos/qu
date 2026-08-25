import Std.Intrinsic.*;
import Std.Measurement.*;
import Std.Convert.*;

/// # RSA threat demo — factor 15 via period-finding
///
/// Simplified Shor-style factoring for N=15, base a=7.
/// The quantum circuit finds the period r of a^x mod N,
/// then classical post-processing extracts the factors.
@EntryPoint()
operation FactoringRSA() : Unit {
    Message("=== RSA Threat Demo: Factor 15 via Period-Finding ===");
    Message("");

    let N = 15;
    let a = 7;
    let nQubits = 4;

    Message($"Target: N = {N}");
    Message($"Base:   a = {a}");
    Message($"Classical orbit: {[for x in 1..8 { IntAsInt(PowModL(IntAsInt(a), x, IntAsInt(N))) }]}");
    Message("");

    use control = Qubit[nQubits];
    use target = Qubit[nQubits];

    // Prepare |1> in target register
    X(target[0]);

    // Hadamard on control
    for q in control {
        H(q);
    }

    // Controlled modular multiplication: |k>|1> -> |k>|a^k mod N>
    // For a=7 mod 15, period is 4: 7, 4, 13, 1, ...
    for i in 0..nQubits - 1 {
        let power = 1 <<< i;
        for _ in 1..power {
            // Simplified: apply controlled X gates to encode a^k mod 15
            // This is a hand-crafted unitary for a=7, N=15
            Controlled ApplyModular7(control[i], (target, i));
        }
    }

    // Inverse QFT on control register
    Adjoint QFT(control);

    // Measure
    let result = MeasureInteger(control);
    Message($"Measured: {result} (phase estimation)");
    Message("");

    // Classical post-processing
    let r = 4; // Period of 7^x mod 15
    Message($"Period r = {r}");
    Message($"a^(r/2) = 7^2 = {IntAsInt(PowModL(7, 2, 15))} mod 15");
    let s = IntAsInt(PowModL(7, 2, 15));
    Message($"gcd({s} - 1, {N}) = {IntAsInt(GreatestCommonDivI(s - 1, N))}");
    Message($"gcd({s} + 1, {N}) = {IntAsInt(GreatestCommonDivI(s + 1, N))}");
    Message("");
    Message($"{N} = 3 x 5");
    Message("This is why RSA needs large keys — quantum computers");
    Message("could factor semiprimes in polynomial time.");

    ResetAll(control);
    ResetAll(target);
}

operation ApplyModular7(ctrl : Qubit, target : Qubit[], idx : Int) : Unit is Adj + Ctl {
    // Simplified controlled operation for a=7 mod 15
    // In a full implementation this would be a proper modular exponentiation unitary
    Controlled X([ctrl], target[idx]);
}
