import Std.Intrinsic.*;
import Std.Math.*;
import Std.Measurement.*;

operation ControlledRotation(control : Qubit, target : Qubit, k : Int) : Unit {
    let angle = PI() / IntAsDouble(1 <<< k);
    Controlled Rz([control], (angle, target));
}

@EntryPoint()
operation QFT() : Unit {
    Message("=== Quantum Fourier Transform (3 qubits) ===");

    use qs = Qubit[3];

    X(qs[0]);
    X(qs[2]);

    Message("Input: |101⟩ = 5");

    H(qs[2]);
    ControlledRotation(qs[1], qs[2], 2);
    ControlledRotation(qs[0], qs[2], 3);

    H(qs[1]);
    ControlledRotation(qs[0], qs[1], 2);

    H(qs[0]);

    Swap(qs[0], qs[2]);

    Message("After QFT:");
    DumpMachine();

    ResetAll(qs);
}
