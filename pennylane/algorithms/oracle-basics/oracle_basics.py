#!/usr/bin/env python3
"""Oracle basics — marking the |11⟩ state with a CZ gate."""
import pennylane as qml

dev = qml.device("default.qubit", wires=2)


@qml.qnode(dev)
def oracle_circuit() -> qml.typing.Result:
    """Prepare |11⟩ and apply the oracle that flips its phase."""
    qml.PauliX(wires=0)
    qml.PauliX(wires=1)
    qml.CZ(wires=[0, 1])
    return qml.state()


@qml.qnode(dev)
def oracle_marking() -> qml.typing.Result:
    """Show the oracle flips phase of |11⟩ but not |00⟩, |01⟩, |10⟩."""
    qml.CZ(wires=[0, 1])
    return qml.state()


def main() -> None:
    print("=== Oracle Basics: Marking |11⟩ ===")
    print()

    print("Oracle applied to |11⟩:")
    print(qml.draw(oracle_circuit)())
    state = oracle_circuit()
    print(f"  State: {state}")
    print(f"  |11⟩ amplitude: {state[3]:.4f}  (phase flipped to -1)")
    print()

    print("Oracle applied to |00⟩ (no flip):")
    print(qml.draw(oracle_marking)())
    state00 = oracle_marking()
    print(f"  State: {state00}")
    print(f"  |00⟩ amplitude: {state00[0]:.4f}  (unchanged)")
    print()

    print("CZ truth table:")
    dev_all = qml.device("default.qubit", wires=2)

    @qml.qnode(dev_all)
    def apply_cz(state: str) -> qml.typing.Result:
        for i, bit in enumerate(state):
            if bit == "1":
                qml.PauliX(wires=i)
        qml.CZ(wires=[0, 1])
        return qml.state()

    for bits in ["00", "01", "10", "11"]:
        s = apply_cz(bits)
        target = int(bits, 2)
        amp = s[target]
        sign = "-" if amp.real < 0 else "+"
        print(f"  CZ|{bits}⟩ = {sign}|{bits}⟩   amp={amp:.1f}")


if __name__ == "__main__":
    main()
