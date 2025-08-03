open Microsoft.Quantum.Canon;
open Microsoft.Quantum.Intrinsic;
// open Microsoft.Quantum.Teleportation;

/// Output
/// The result of a Z-basis measurement on the teleported qubit,
/// represented as a Bool.
operation TeleportClassicalMessage(message : Bool) : Bool {
    mutable measurement = false;
    use register = Qubit[2] {

        let msg = register[0];
        let there = register[1];

        // Encode the message we want to send.
        if (message) { X(msg); }

        // Create a Bell pair between msg and there
        H(there);
        CNOT(there, msg);

        // Bell measurement on msg
        CNOT(msg, there);
        H(msg);

        // Send classical bits (simulate by measuring)
        let m1 = M(msg);
        let m2 = M(there);

        // Apply corrections
        if (m2 == One) { X(there); }
        if (m1 == One) { Z(there); }

        if (M(there) == One) { set measurement = true; }

        ResetAll(register);
    }
    return measurement;
}
