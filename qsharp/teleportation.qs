import Std.Diagnostics.*;
import Std.Intrinsic.*;
import Std.Measurement.*;

operation Main() : Result[] {
    let stateInitializerBasisTuples = [
        ("|0〉", I, PauliZ),
        ("|1〉", X, PauliZ),
        ("|+〉", SetToPlus, PauliX),
        ("|-〉", SetToMinus, PauliX)
    ];

    mutable results = [];
    for (state, initializer, basis) in stateInitializerBasisTuples {
        use (message, target) = (Qubit(), Qubit());

        initializer(message);
        Message($"Teleporting state {state}");
        DumpRegister([message]);

        Teleport(message, target);
        Message($"Received state {state}");
        DumpRegister([target]);

        let result = Measure([basis], [target]);
        set results += [result];
        ResetAll([message, target]);
    }

    return results;
}

operation Teleport(message : Qubit, target : Qubit) : Unit {
    use auxiliary = Qubit();

    H(auxiliary);
    CNOT(auxiliary, target);

    CNOT(message, auxiliary);
    H(message);

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

// open Microsoft.Quantum.Canon;
// open Microsoft.Quantum.Intrinsic;
// open Microsoft.Quantum.Measurement;

// // open Microsoft.Quantum.Teleportation;

// operation Teleport(msg : Qubit, there : Qubit) : Unit {
//     use register = Qubit[1] {
//         // Ask for an auxiliary qubit that we can use to prepare
//         // for teleportation.
//         let here = register[0];

//         // Create some entanglement that we can use to send our message.
//         H(here);
//         CNOT(here, there);

//         // Move our message into the entangled pair.
//         CNOT(msg, here);
//         H(msg);

//         // Measure out the entanglement.
//         if (M(msg) == One) { Z(there); }
//         if (M(here) == One) { X(there); }

//         // Reset our "here" qubit before releasing it.
//         Reset(here);
//     }
// }

// /// Output
// /// The result of a Z-basis measurement on the teleported qubit,
// /// represented as a Bool.
// operation TeleportClassicalMessage(message : Bool) : Bool {
//     mutable measurement = false;
//     use register = Qubit[2] {

//         let msg = register[0];
//         let there = register[1];

//         // Encode the message we want to send.
//         if (message) { X(msg); }

//         // Create a Bell pair between msg and there
//         H(there);
//         CNOT(there, msg);

//         // Bell measurement on msg
//         CNOT(msg, there);
//         H(msg);

//         // Send classical bits (simulate by measuring)
//         let m1 = M(msg);
//         let m2 = M(there);

//         // Apply corrections
//         if (m2 == One) { X(there); }
//         if (m1 == One) { Z(there); }

//         if (M(there) == One) { set measurement = true; }

//         ResetAll(register);
//     }
//     return measurement;
// }