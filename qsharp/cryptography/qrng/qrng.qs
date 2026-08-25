import Std.Intrinsic.*;
import Std.Measurement.*;
import Std.Convert.*;

/// # Quantum Random Number Generation
///
/// Measure Hadamard-created superpositions to extract truly random bits.
/// Quantum measurement outcomes are inherently unpredictable.
@EntryPoint()
operation QRNG() : Unit {
    Message("=== Quantum Random Number Generator ===");
    Message("");

    // Generate 16 random bits
    Message("16 random bits:");
    mutable bits = "";
    for _ in 1..16 {
        use q = Qubit();
        H(q);
        let result = M(q);
        if result == One {
            set bits += "1";
        } else {
            set bits += "0";
        }
        Reset(q);
    }
    Message($"  {bits}");

    // Generate 1000 bits and check frequency
    Message("");
    Message("Frequency test (1000 bits):");
    mutable ones = 0;
    for _ in 1..1000 {
        use q = Qubit();
        H(q);
        if M(q) == One {
            set ones += 1;
        }
        Reset(q);
    }
    let zeros = 1000 - ones;
    Message($"  0s: {zeros}, 1s: {ones}");

    // Chi-squared test
    let expected = 500.0;
    let chi2 = (IntAsDouble((zeros - 500) * (zeros - 500)) + IntAsDouble((ones - 500) * (ones - 500))) / expected;
    Message($"  Chi-squared: {chi2}");
    Message($"  Critical value (p=0.05): 3.841");
    if chi2 < 3.841 {
        Message("  PASS — distribution is uniform");
    } else {
        Message("  FAIL — distribution is biased");
    }

    Message("");
    Message("Quantum RNG: measurement outcomes are inherently");
    Message("unpredictable — no classical algorithm can reproduce them.");
}
