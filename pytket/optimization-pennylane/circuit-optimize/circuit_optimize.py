from pytket import Circuit
from pytket.passes import FullPeepholeOptimise, RemoveRedundancies
from pytket.qenn import tk_to_qenn, qenn_to_tk

import pennylane as qml
import numpy as np


def build_pennylane_circuit() -> qml.tape.QuantumTape:
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.PauliX(wires=0)
        qml.PauliX(wires=0)
        qml.Hadamard(wires=1)
        qml.Hadamard(wires=1)
        qml.CNOT(wires=[2, 0])
        qml.T(wires=0)
        qml.adjoint(qml.T)(wires=0)
        return qml.expval(qml.PauliZ(0))

    return circuit.tape


def tape_info(tape: qml.tape.QuantumTape) -> dict:
    ops = tape.operations
    gate_names = [op.name for op in ops]
    return {"gates": len(ops), "depth": tape.depth, "ops": dict(sorted(
        {n: gate_names.count(n) for n in set(gate_names)}.items()
    ))}


def circuit_info_tket(c: Circuit) -> dict:
    ops = {}
    for g in c.get_commands():
        name = g.op.type.__name__
        ops[name] = ops.get(name, 0) + 1
    return {"gates": c.n_gates, "depth": c.depth(), "ops": dict(sorted(ops.items()))}


def main() -> None:
    tape = build_pennylane_circuit()
    before = tape_info(tape)
    print("=== PennyLane tape (before) ===")
    print(qml.draw(tape)())
    print(f"  gates={before['gates']}  depth={before['depth']}")
    print(f"  ops={before['ops']}")
    print()

    tk_circ = qenn_to_tk(tape)
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

    tape_opt = tk_to_qenn(tk_circ)
    after = tape_info(tape_opt)
    print("=== PennyLane tape (after) ===")
    print(qml.draw(tape_opt)())
    print(f"  gates={after['gates']}  depth={after['depth']}")
    print(f"  ops={after['ops']}")
    print()

    print(f"Gate reduction: {before['gates']} -> {after['gates']} "
          f"({before['gates'] - after['gates']} gates removed)")


if __name__ == "__main__":
    main()
