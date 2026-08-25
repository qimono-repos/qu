// Big-O in Q# — O(1) and O(log n) quantum operations
//
// Run: qsharp run big_o.qs

import Std.Intrinsic.*;
import Std.Measurement.*;

@EntryPoint()
operation BigOExamples() : Result[] {
    Message("=== Big-O in Quantum Computing ===\n");

    // O(1) — Constant time: single-qubit measurement
    Message("O(1) — Measure one qubit:");
    use q1 = Qubit();
    H(q1);
    let r1 = M(q1);
    Reset(q1);
    Message($"  Result: {r1}\n");

    // O(log n) — Grover's search on 3 qubits (N=8)
    // The oracle marks |101⟩ = |5⟩
    Message("O(log n) — Grover search on 3 qubits (N=8), marking |101⟩:");
    let result = GroverSearch();
    Message($"  Found: {result}\n");

    return [r1];
}

operation GroverSearch() : Result {
    use qubits = Qubit[3];

    // Initialize uniform superposition
    for q in qubits {
        H(q);
    }

    // Grover iteration (1 iteration is optimal for N=8, 1 solution)
    // Oracle: flip phase of |101⟩
    X(qubits[1]);              // mark qubit 1 (middle qubit = |0⟩ -> need X)
    Controlled Z([qubits[0]], qubits[2]);  // multi-controlled Z
    X(qubits[1]);              // undo X

    // Diffusion operator
    for q in qubits {
        H(q);
    }
    for q in qubits {
        X(q);
    }
    Controlled Z([qubits[0]], qubits[2]);
    for q in qubits {
        X(q);
    }
    for q in qubits {
        H(q);
    }

    // Measure
    let result = M(qubits[0]);
    ResetAll(qubits);
    return result;
}
