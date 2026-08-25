import Std.Intrinsic.*;
import Std.Measurement.*;

/// # BB84 Quantum Key Distribution Protocol
///
/// Alice encodes random bits in random bases, Bob measures in random bases.
/// They publicly compare bases, keep matching ones, then check QBER.
@EntryPoint()
operation BB84() : Unit {
    Message("=== BB84 Quantum Key Distribution ===");
    Message("");

    let numBits = 16;

    use aliceQubits = Qubit[numBits];
    use bobResults = Qubit[numBits];

    mutable aliceBits = Repeated(false, numBits);
    mutable aliceBases = Repeated(false, numBits);
    mutable bobBases = Repeated(false, numBits);

    // Alice: prepare qubits in random states
    for i in 0..numBits - 1 {
        let bit = DrawRandomBool(0.5);
        let basisZ = DrawRandomBool(0.5);

        set aliceBits = w/ i <- bit;
        set aliceBases = w/ i <- basisZ;

        if bit {
            X(aliceQubits[i]);
        }
        if not basisZ {
            H(aliceQubits[i]);
        }
    }

    // Bob: measure in random bases
    for i in 0..numBits - 1 {
        let basisZ = DrawRandomBool(0.5);
        set bobBases = w/ i <- basisZ;

        if not basisZ {
            H(aliceQubits[i]);
        }

        let result = M(aliceQubits[i]);
        set bobResults = w/ i <- result == One;
    }

    // Sift: keep matching bases
    mutable keyAlice = [];
    mutable keyBob = [];

    for i in 0..numBits - 1 {
        if aliceBases[i] == bobBases[i] {
            set keyAlice += [aliceBits[i]];
            set keyBob += [bobResults[i]];
        }
    }

    Message($"Sifted key length: {Length(keyAlice)}");
    Message($"Alice's key: {keyAlice}");
    Message($"Bob's key:   {keyBob}");

    // Check QBER on a subset
    let checkBits = Min(4, Length(keyAlice));
    mutable errors = 0;

    for i in 0..checkBits - 1 {
        if keyAlice[i] != keyBob[i] {
            set errors += 1;
        }
    }

    Message("");
    Message($"Check bits: {checkBits}, errors: {errors}");
    if errors > checkBits / 2 {
        Message("EAVESDROPPING DETECTED!");
    } else {
        Message("QBER acceptable — key is secure.");
    }

    ResetAll(aliceQubits);
    ResetAll(bobResults);
}

function Min(a : Int, b : Int) : Int {
    if a < b { a } else { b }
}
