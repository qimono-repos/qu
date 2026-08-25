import numpy as np

from bloqade.analog import AtomArrangement, Sequence
from bloqade.analog.emulator import Emulator


def build_sequence(spacing_um: float, detuning_mhz: float) -> Sequence:
    n_atoms = 4
    atoms = AtomArrangement()
    for i in range(n_atoms):
        atoms.add(x=i * spacing_um, y=0.0)

    seq = Sequence(atoms)
    seq.set.uniform.rabi.frequency.value = 2 * np.pi * 1.0
    seq.set.uniform.detuning.value = 2 * np.pi * 0.0
    seq.set.uniform.rabi.frequency.value = 0.0
    seq.set.uniform.detuning.value = 2 * np.pi * detuning_mhz
    seq.measure.basis = "ground-rydberg"
    return seq


def main() -> None:
    spacings = [4.0, 6.0, 8.0, 10.0]
    detuning_mhz = -1.0

    device = Emulator()

    print("Parameter sweep: atom spacing vs. Rydberg population")
    print(f"  Detuning: 2π × {detuning_mhz} MHz (constant)")
    print(f"  Spacings: {spacings} µm")
    print()

    for spacing in spacings:
        seq = build_sequence(spacing, detuning_mhz)
        job = device.run(seq)
        result = job.report()
        mean_pop = result.mean()
        print(f"  spacing = {spacing:5.1f} µm → mean Rydberg pop = {mean_pop:.4f}")

    print()
    print("Small spacing: blockade suppresses excitations (ordered phase).")
    print("Large spacing: atoms act independently (disordered phase).")


if __name__ == "__main__":
    main()
