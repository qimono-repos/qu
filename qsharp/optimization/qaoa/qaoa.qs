import Std.Intrinsic.*;
import Std.Measurement.*;
import Std.Convert.*;

/// QAOA for MaxCut on C4 (0-1-2-3-0) — simplified demonstration.
///
/// QAOA alternates between a cost unitary (encoding the MaxCut objective)
/// and a mixer unitary.  This implementation uses a fixed two-layer
/// QAOA circuit with illustrative parameters.
///
/// MaxCut on C4: the optimal cut is 4 (all edges cut).
/// Graph edges: (0,1), (1,2), (2,3), (3,0)

operation CostLayer(qubits : Qubit[], gamma : Double) : Unit {
    let n = Length(qubits);
    for i in 0..n - 1 {
        let j = (i + 1) % n;
        CNOT(qubits[i], qubits[j]);
        Rz(2.0 * gamma, qubits[j]);
        CNOT(qubits[i], qubits[j]);
    }
}

operation MixerLayer(qubits : Qubit[], beta : Double) : Unit {
    for q in qubits {
        Rx(2.0 * beta, q);
    }
}

operation QAOACircuit(qubits : Qubit[], gammas : Double[], betas : Double[]) : Unit {
    let p = Length(gammas);
    for q in qubits {
        H(q);
    }
    for k in 0..p - 1 {
        CostLayer(qubits, gammas[k]);
        MixerLayer(qubits, betas[k]);
    }
}

function FormatResult(bit : Result) : String {
    if bit == Zero {
        "0"
    } else {
        "1"
    }
}

@EntryPoint()
operation QAOA() : Unit {
    Message("=== QAOA MaxCut on C4 ===");
    Message("Edges: (0,1) (1,2) (2,3) (3,0)");
    Message("Optimal cut: 4 (all edges)");
    Message("");

    use qubits = Qubit[4];

    let gammas = [0.5, 0.8];
    let betas  = [0.3, 0.6];

    Message($"Parameters: gammas={gammas}, betas={betas}");
    Message("");

    QAOACircuit(qubits, gammas, betas);

    let r0 = M(qubits[0]);
    let r1 = M(qubits[1]);
    let r2 = M(qubits[2]);
    let r3 = M(qubits[3]);

    let bits = [r0, r1, r2, r3];
    let bitStr = FormatResult(r0) + FormatResult(r1)
                 + FormatResult(r2) + FormatResult(r3);

    Message($"Measured: |{bitStr}⟩");
    Message("");

    mutable cutCount = 0;
    let edges = [(0, 1), (1, 2), (2, 3), (3, 0)];
    for (i, j) in edges {
        if bits[i] != bits[j] {
            set cutCount += 1;
            Message($"  Edge ({i},{j}): CUT (qubits differ)");
        } else {
            Message($"  Edge ({i},{j}): uncut (qubits same)");
        }
    }
    Message("");
    Message($"Cut value: {cutCount} / 4");

    ResetAll(qubits);
}
