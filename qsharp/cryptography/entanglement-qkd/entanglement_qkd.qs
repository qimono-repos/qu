import Std.Intrinsic.*;
import Std.Measurement.*;

/// # E91 Entanglement-Based QKD
///
/// Alice and Bob share Bell pairs. Each measures in a randomly chosen basis.
/// After public comparison they keep matching bases and extract a key.
@EntryPoint()
operation E91QKD() : Unit {
    Message("=== E91 Entanglement-Based QKD ===");
    Message("");

    let numPairs = 20;

    use aliceQubits = Qubit[numPairs];
    use bobQubits = Qubit[numPairs];

    mutable aliceBases = Repeated(0, numPairs);
    mutable bobBases = Repeated(0, numPairs);
    mutable aliceResults = Repeated(false, numPairs);
    mutable bobResults = Repeated(false, numPairs);

    for i in 0..numPairs - 1 {
        // Create Bell pair
        H(aliceQubits[i]);
        CNOT(aliceQubits[i], bobQubits[i]);

        // Random bases (0=Z, 1=X, 2=diagonal)
        let aBasis = DrawRandomInt(0, 2);
        let bBasis = DrawRandomInt(0, 2);
        set aliceBases = w/ i <- aBasis;
        set bobBases = w/ i <- bBasis;

        // Alice measures
        if aBasis == 1 {
            H(aliceQubits[i]);
        } elif aBasis == 2 {
            // Approximate diagonal basis with Ry(pi/4)
            // In full implementation, would use proper rotation
            H(aliceQubits[i]);
            S(aliceQubits[i]);
        }
        let aResult = M(aliceQubits[i]);
        set aliceResults = w/ i <- aResult == One;

        // Bob measures
        if bBasis == 1 {
            H(bobQubits[i]);
        } elif bBasis == 2 {
            H(bobQubits[i]);
            S(bobQubits[i]);
        }
        let bResult = M(bobQubits[i]);
        set bobResults = w/ i <- bResult == One;
    }

    // Sift: keep matching bases
    mutable keyAlice = [];
    mutable keyBob = [];

    for i in 0..numPairs - 1 {
        if aliceBases[i] == bobBases[i] {
            set keyAlice += [aliceResults[i]];
            set keyBob += [bobResults[i]];
        }
    }

    Message($"Matching basis pairs: {Length(keyAlice)}/{numPairs}");
    Message($"Alice's key: {keyAlice}");
    Message($"Bob's key:   {keyBob}");

    // Check correlations
    mutable errors = 0;
    let checkBits = Min(4, Length(keyAlice));
    for i in 0..checkBits - 1 {
        if keyAlice[i] != keyBob[i] {
            set errors += 1;
        }
    }

    Message("");
    Message($"QBER: {errors}/{checkBits}");
    if errors > checkBits / 2 {
        Message("Eavesdropping detected!");
    } else {
        let finalLen = Length(keyAlice) - checkBits;
        Message($"Secure key ({finalLen} bits)");
    }

    ResetAll(aliceQubits);
    ResetAll(bobQubits);
}

function Min(a : Int, b : Int) : Int {
    if a < b { a } else { b }
}
