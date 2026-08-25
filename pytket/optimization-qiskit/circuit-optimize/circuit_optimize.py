from pytket import Circuit
from pytket.passes import FullPeepholeOptimise, RemoveRedundancies
from pytket.qiskit import qiskit_to_tk, tk_to_qiskit

import qiskit as qk


def build_qiskit_circuit() -> qk.QuantumCircuit:
    qc = qk.QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.x(0)
    qc.x(0)
    qc.h(1)
    qc.h(1)
    qc.cx(2, 0)
    qc.t(0)
    qc.tdg(0)
    return qc


def circuit_info_qiskit(qc: qk.QuantumCircuit) -> dict:
    data = qc.data
    gate_names = [inst.operation.name for inst in data]
    return {"gates": len(data), "depth": qc.depth(), "ops": dict(sorted(
        {n: gate_names.count(n) for n in set(gate_names)}.items()
    ))}


def circuit_info_tket(c: Circuit) -> dict:
    ops = {}
    for g in c.get_commands():
        name = g.op.type.__name__
        ops[name] = ops.get(name, 0) + 1
    return {"gates": c.n_gates, "depth": c.depth(), "ops": dict(sorted(ops.items()))}


def main() -> None:
    qc = build_qiskit_circuit()
    before = circuit_info_qiskit(qc)
    print("=== Qiskit circuit (before) ===")
    print(qc.draw())
    print(f"  gates={before['gates']}  depth={before['depth']}")
    print(f"  ops={before['ops']}")
    print()

    tk_circ = qiskit_to_tk(qc)
    tk_before = circuit_info_tket(tk_circ)
    print("=== pytket after import ===")
    print(f"  gates={tk_before['gates']}  depth={tk_before['depth']}")
    print()

    FullPeepholeOptimise().apply(tk_circ)
    RemoveRedundancies().apply(tk_circ)
    tk_after = circuit_info_tket(tk_circ)
    print("=== pytket after FullPeepholeOptimise + RemoveRedundancies ===")
    print(f"  gates={tk_after['gates']}  depth={tk_after['depth']}")
    print(f"  ops={tk_after['ops']}")
    print()

    qc_opt = tk_to_qiskit(tk_circ)
    after = circuit_info_qiskit(qc_opt)
    print("=== Qiskit circuit (after) ===")
    print(qc_opt.draw())
    print(f"  gates={after['gates']}  depth={after['depth']}")
    print(f"  ops={after['ops']}")
    print()

    print(f"Gate reduction: {before['gates']} -> {after['gates']} "
          f"({before['gates'] - after['gates']} gates removed)")


if __name__ == "__main__":
    main()
