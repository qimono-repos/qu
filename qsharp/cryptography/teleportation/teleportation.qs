import Std.Diagnostics.*;
import Std.Intrinsic.*;
import Std.Measurement.*;

/// # Quantum Teleportation Protocol
///
/// Teleport an arbitrary state from Alice to Bob using a Bell pair
/// and classical corrections. Tests multiple states.
@EntryPoint()
operation TeleportationMain() : Unit {
    Message("=== Quantum Teleportation ===");
    Message("");

    let stateInitializerBasisTuples = [
        ("|0>", I, PauliZ),
        ("|1>", X, PauliZ),
        ("|+>", SetToPlus, PauliX),
        ("|-)", SetToMinus, PauliX)
    ];

    for (state, initializer, basis) in stateInitializerBasisTuples {
        use (message, target) = (Qubit(), Qubit());

        initializer(message);
        Message($"Teleporting state {state}");
        DumpRegister([message]);

        Teleport(message, target);
        Message($"Received state {state}");
        DumpRegister([target]);

        let result = Measure([basis], [target]);
        Message($"  Measured: {result}");
        Message("");

        ResetAll([message, target]);
    }
}

/// Teleport the state of `message` to `target` using an auxiliary qubit.
operation Teleport(message : Qubit, target : Qubit) : Unit {
    use auxiliary = Qubit();

    // Create Bell pair between auxiliary and target
    H(auxiliary);
    CNOT(auxiliary, target);

    // Bell measurement on message and auxiliary
    CNOT(message, auxiliary);
    H(message);

    // Classical corrections
    if M(auxiliary) == One {
        X(target);
    }
    if M(message) == One {
        Z(target);
    }

    Reset(auxiliary);
}

operation SetToPlus(q : Qubit) : Unit is Adj + Ctl {
    H(q);
}

operation SetToMinus(q : Qubit) : Unit is Adj + Ctl {
    X(q);
    H(q);
}
