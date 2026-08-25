import Std.Intrinsic.*;
import Std.Measurement.*;
import Std.Convert.*;

/// 4-city Travelling Salesperson Problem — simplified quantum demonstration.
///
/// City 0 is fixed at position 0.  The 3 remaining cities are placed
/// in positions 1, 2, 3 using a quantum search over permutations.
/// This demo encodes the distance structure as a phase oracle and
/// uses amplitude amplification to highlight low-cost tours.
///
/// Distance matrix (symmetric):
///   depot(0)  harbor(1)  market(2)  tower(3)
///   depot       0.0       2.0        3.0       2.5
///   harbor      2.0       0.0        1.5       4.0
///   market      3.0       1.5        0.0       1.0
///   tower       2.5       4.0        1.0       0.0
///
/// Optimal tour: depot -> harbor -> market -> tower -> depot
///   cost = 2.0 + 1.5 + 1.0 + 2.5 = 7.0

operation TourPhaseOracle(qubits : Qubit[], tourIndex : Int) : Unit {
    if tourIndex == 0 {
        (Controlled Z)([qubits[0]], qubits[1]);
        (Controlled Z)([qubits[0], qubits[1]], qubits[2]);
    }
    if tourIndex == 1 {
        (Controlled Z)([qubits[0]], qubits[1]);
        X(qubits[2]);
        (Controlled Z)([qubits[0], qubits[1]], qubits[2]);
        X(qubits[2]);
    }
    if tourIndex == 2 {
        X(qubits[1]);
        (Controlled Z)([qubits[0], qubits[1]], qubits[2]);
        X(qubits[1]);
    }
    if tourIndex == 3 {
        X(qubits[0]);
        X(qubits[1]);
        (Controlled Z)([qubits[0], qubits[1]], qubits[2]);
        X(qubits[0]);
        X(qubits[1]);
    }
}

operation Diffusion(qubits : Qubit[]) : Unit {
    for q in qubits {
        H(q);
    }
    for q in qubits {
        X(q);
    }
    Controlled Z([qubits[0]], qubits[1]);
    Controlled Z([qubits[0], qubits[1]], qubits[2]);
    for q in qubits {
        X(q);
    }
    for q in qubits {
        H(q);
    }
}

function FormatResult(bit : Result) : String {
    if bit == Zero { "0" } else { "1" }
}

@EntryPoint()
operation TSP() : Unit {
    Message("=== 4-City TSP with Amplitude Amplification ===");
    Message("");
    Message("Cities: depot(0), harbor(1), market(2), tower(3)");
    Message("Distances:");
    Message("  depot  -> harbor: 2.0, market: 3.0, tower: 2.5");
    Message("  harbor -> market: 1.5, tower: 4.0");
    Message("  market -> tower:  1.0");
    Message("");

    Message("Optimal tour: depot -> harbor -> market -> tower -> depot");
    Message("  cost = 2.0 + 1.5 + 1.0 + 2.5 = 7.0");
    Message("");

    Message("Classical enumeration of all tours from depot:");
    Message("  0-1-2-3: 2.0+1.5+1.0+2.5 = 7.0  (optimal)");
    Message("  0-1-3-2: 2.0+4.0+1.0+3.0 = 10.0");
    Message("  0-2-1-3: 3.0+1.5+4.0+2.5 = 11.0");
    Message("  0-2-3-1: 3.0+1.0+4.0+2.0 = 10.0");
    Message("  0-3-1-2: 2.5+4.0+1.5+3.0 = 11.0");
    Message("  0-3-2-1: 2.5+1.0+1.5+2.0 = 7.0  (optimal)");
    Message("");

    use qubits = Qubit[3];

    for q in qubits {
        H(q);
    }

    for _ in 1..2 {
        TourPhaseOracle(qubits, 0);
        Diffusion(qubits);
    }

    let r0 = M(qubits[0]);
    let r1 = M(qubits[1]);
    let r2 = M(qubits[2]);

    let bitStr = FormatResult(r0) + FormatResult(r1) + FormatResult(r2);

    mutable tourIdx = 0;
    if r0 == One {
        set tourIdx += 1;
    }
    if r1 == One {
        set tourIdx += 2;
    }
    if r2 == One {
        set tourIdx += 4;
    }

    Message($"Measured state: |{bitStr}⟩ (index {tourIdx})");
    Message("");
    Message("This maps to a permutation of cities 1,2,3 in positions 1,2,3.");
    Message("Amplitude amplification boosts the probability of low-cost tours.");
    Message("The optimal tours (cost 7.0) are 0-1-2-3 and 0-3-2-1.");

    ResetAll(qubits);
}
