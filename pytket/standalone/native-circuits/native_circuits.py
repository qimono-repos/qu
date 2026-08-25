from pytket import Circuit
from pytket.passes import (
    FullPeepholeOptimise,
    RemoveRedundancies,
    CommuteThroughMultis,
    CliffordSimp,
)


def circuit_info(c: Circuit) -> dict:
    ops = {}
    for g in c.get_commands():
        name = g.op.type.__name__
        ops[name] = ops.get(name, 0) + 1
    return {"gates": c.n_gates, "depth": c.depth(), "ops": dict(sorted(ops.items()))}


def build_bell_circuit() -> Circuit:
    c = Circuit(2)
    c.H(0)
    c.CX(0, 1)
    return c


def build_entangled_with_redundancy() -> Circuit:
    c = Circuit(3)
    c.H(0)
    c.CX(0, 1)
    c.CX(1, 2)
    c.X(0)
    c.X(0)
    c.H(1)
    c.H(1)
    c.CX(2, 0)
    c.T(0)
    c.Tdg(0)
    return c


def build_variational_ansatz() -> Circuit:
    c = Circuit(3)
    c.Rx(0.5, 0)
    c.Ry(0.3, 1)
    c.Rz(0.7, 2)
    c.CX(0, 1)
    c.CX(1, 2)
    c.Rx(0.2, 0)
    c.Ry(0.4, 1)
    c.Rz(0.6, 2)
    c.CX(0, 2)
    c.H(0)
    c.S(1)
    c.T(2)
    return c


def print_section(title: str) -> None:
    print(f"{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_info(label: str, info: dict) -> None:
    print(f"  {label}: gates={info['gates']}  depth={info['depth']}")
    print(f"  ops={info['ops']}")
    print()


def optimize(c: Circuit, level: int) -> Circuit:
    c_opt = c.copy()
    if level >= 1:
        RemoveRedundancies().apply(c_opt)
    if level >= 2:
        CommuteThroughMultis().apply(c_opt)
        RemoveRedundancies().apply(c_opt)
    if level >= 3:
        CliffordSimp().apply(c_opt)
        RemoveRedundancies().apply(c_opt)
    if level >= 4:
        FullPeepholeOptimise().apply(c_opt)
        RemoveRedundancies().apply(c_opt)
    return c_opt


def demo_circuit(name: str, builder) -> None:
    c = builder()
    print_section(name)
    print_info("Before", circuit_info(c))

    for level in range(5):
        c_opt = optimize(c, level)
        info = circuit_info(c_opt)
        print_info(f"Level {level}", info)


def main() -> None:
    demo_circuit("Bell circuit (2 qubits)", build_bell_circuit)
    demo_circuit("Entangled + redundant (3 qubits)", build_entangled_with_redundancy)
    demo_circuit("Variational ansatz (3 qubits)", build_variational_ansatz)

    print_section("Summary")
    c = build_entangled_with_redundancy()
    before = circuit_info(c)
    c_opt = optimize(c, 4)
    after = circuit_info(c_opt)
    print(f"  Entangled: {before['gates']} -> {after['gates']} gates "
          f"({before['gates'] - after['gates']} removed)")
    c = build_variational_ansatz()
    before = circuit_info(c)
    c_opt = optimize(c, 4)
    after = circuit_info(c_opt)
    print(f"  Variational: {before['gates']} -> {after['gates']} gates "
          f"({before['gates'] - after['gates']} removed)")


if __name__ == "__main__":
    main()
