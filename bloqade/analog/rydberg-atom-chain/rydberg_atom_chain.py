import numpy as np

from bloqade.analog import AtomArrangement, Sequence
from bloqade.analog.emulator import Emulator


def build_chain(spacing_um: float = 6.0) -> Sequence:
    n_atoms = 4
    positions = [(i * spacing_um, 0.0) for i in range(n_atoms)]

    atoms = AtomArrangement()
    for x, y in positions:
        atoms.add(x=x, y=y)

    seq = Sequence(atoms)
    seq.set.uniform.rabi.frequency.value = 2 * np.pi * 1.0
    seq.set.uniform.detuning.value = 2 * np.pi * 0.0
    seq.set.uniform.rabi.frequency.value = 0.0
    seq.set.uniform.detuning.value = 2 * np.pi * -3.0
    seq.measure.basis = "ground-rydberg"
    return seq


def main() -> None:
    seq = build_chain(spacing_um=6.0)
    device = Emulator()
    job = device.run(seq)
    result = job.report()

    print("Rydberg atom chain (4 atoms, spacing 6.0 µm):")
    print(f"  Rabi frequency: 2π × 1.0 MHz (on), then 0 MHz (off)")
    print(f"  Detuning:       2π × 0.0 MHz (on), then 2π × -3.0 MHz (off)")
    print()
    print(f"Bitstrings: {result.counts}")
    print(f"Mean rydberg population: {result.mean()}")


if __name__ == "__main__":
    main()
