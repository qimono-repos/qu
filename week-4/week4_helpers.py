"""Shared, non-graded helpers for the Week 4 notebooks.

Nothing in this module builds the four N=1 Deutsch-Jozsa oracles. Albert writes
those by hand and commits them only after the lab is submitted. The helpers here
only simulate, format, and check circuits that the learner supplies.
"""

from __future__ import annotations

import cmath
import math
from collections import Counter
from typing import Iterable

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector


def run_counts(
    circuit: QuantumCircuit, shots: int = 1024, seed: int = 42
) -> dict[str, int]:
    """Return measurement counts, using Aer when available.

    Aer gives a reproducible simulator seed. If Aer is not installed, fall back
    to Qiskit's ideal ``StatevectorSampler``. The fallback is still reproducible
    enough for teaching histograms, but it does not expose a simulator seed.
    """
    try:
        from qiskit_aer import AerSimulator

        simulator = AerSimulator()
        result = simulator.run(
            circuit, shots=shots, seed_simulator=seed
        ).result()
        return dict(result.get_counts())
    except ImportError:
        from qiskit.primitives import StatevectorSampler

        result = StatevectorSampler().run([circuit], shots=shots).result()
        data = result[0].data
        for name in ("meas", "measure", "c"):
            register = getattr(data, name, None)
            if register is not None and hasattr(register, "get_counts"):
                return dict(register.get_counts())
        raise RuntimeError(
            "The circuit has no measurement to sample. Add measurements first."
        )


def probabilities(counts: dict[str, int], shots: int | None = None) -> dict[str, float]:
    """Convert counts to probabilities, inferring the number of shots when needed."""
    total = shots if shots is not None else sum(counts.values())
    if total <= 0:
        raise ValueError("Counts are empty; there is nothing to normalize.")
    return {bitstring: count / total for bitstring, count in counts.items()}


def total_variation_distance(
    first: dict[str, float], second: dict[str, float]
) -> float:
    """Return half the L1 distance between two distributions over bitstrings."""
    keys = set(first) | set(second)
    return 0.5 * sum(abs(first.get(key, 0.0) - second.get(key, 0.0)) for key in keys)


def statevector_table(
    circuit: QuantumCircuit, atol: float = 1e-9
) -> list[tuple[str, complex]]:
    """Return ``(bitstring, amplitude)`` pairs after dropping final measurements."""
    clean = circuit.copy()
    clean.remove_final_measurements(inplace=True)
    state = Statevector.from_instruction(clean)
    num_qubits = clean.num_qubits
    rows: list[tuple[str, complex]] = []
    for index, amplitude in enumerate(state.data):
        if abs(amplitude) <= atol:
            continue
        rows.append((format(index, f"0{num_qubits}b"), complex(amplitude)))
    return rows


def _exact_real(value: float, atol: float = 1e-9) -> str | None:
    """Return a small exact-looking string for common real magnitudes."""
    table = (
        (1.0, "1"),
        (0.5, "1/2"),
        (0.25, "1/4"),
        (1 / math.sqrt(2), "1/√2"),
        (1 / (2 * math.sqrt(2)), "1/(2√2)"),
        (math.sqrt(2) / 2, "1/√2"),
        (math.sqrt(2) / 4, "1/(2√2)"),
    )
    for exact, label in table:
        if abs(value - exact) <= atol:
            return label
    return None


def format_amplitude(amplitude: complex, atol: float = 1e-9) -> str:
    """Format a statevector amplitude using recognizable exact forms.

    Examples: ``0``, ``1/√2``, ``-1/√2``, ``i/√2``, ``-i/2``, ``1``.
    Anything else falls back to a readable decimal form.
    """
    amplitude = complex(amplitude)
    if abs(amplitude) <= atol:
        return "0"

    magnitude = abs(amplitude)
    phase = cmath.phase(amplitude)
    magnitude_label = _exact_real(magnitude, atol=atol)

    if magnitude_label is not None:
        if abs(phase) <= atol:
            return magnitude_label
        if abs(abs(phase) - math.pi) <= atol:
            return f"-{magnitude_label}"
        if abs(phase - math.pi / 2) <= atol:
            return f"i·{magnitude_label}"
        if abs(phase + math.pi / 2) <= atol:
            return f"-i·{magnitude_label}"

    if abs(amplitude.imag) <= atol:
        return f"{amplitude.real:.4f}"
    if abs(amplitude.real) <= atol:
        return f"{amplitude.imag:+.4f}i"
    return f"{amplitude.real:.4f}{amplitude.imag:+.4f}i"


def print_statevector(circuit: QuantumCircuit, atol: float = 1e-9) -> None:
    """Print the non-zero amplitudes of a circuit in computational-basis order."""
    print(f"{'bitstring':>10}  {'amplitude':>14}")
    print("-" * 28)
    for bitstring, amplitude in statevector_table(circuit, atol=atol):
        print(f"{bitstring:>10}  {format_amplitude(amplitude, atol=atol):>14}")


def deutsch_jozsa_circuit(oracle: QuantumCircuit, n: int) -> QuantumCircuit:
    """Wrap a learner-supplied oracle in the Deutsch-Jozsa circuit.

    ``oracle`` must act on ``n + 1`` qubits: data qubits ``0 .. n-1`` and the
    ancilla on qubit ``n``. This function never constructs an oracle.
    """
    if oracle.num_qubits != n + 1:
        raise ValueError(
            f"oracle must have {n + 1} qubits (data + ancilla), "
            f"but it has {oracle.num_qubits}."
        )
    circuit = QuantumCircuit(n + 1, n)
    circuit.x(n)
    circuit.h(range(n + 1))
    circuit.compose(oracle, qubits=range(n + 1), inplace=True)
    circuit.h(range(n))
    circuit.measure(range(n), range(n))
    return circuit


def oracle_truth_table(
    oracle: QuantumCircuit, n: int, atol: float = 1e-8
) -> list[tuple[str, int]]:
    """Check a learner-supplied oracle by reading out ``f(x)`` for every ``x``.

    The oracle is assumed to map ``|x, 0>`` to ``|x, f(x)>`` on data qubits
    ``0 .. n-1`` and ancilla ``n``. This is a checker, not a generator.
    """
    if oracle.num_qubits != n + 1:
        raise ValueError(
            f"oracle must have {n + 1} qubits (data + ancilla), "
            f"but it has {oracle.num_qubits}."
        )

    table: list[tuple[str, int]] = []
    for x in range(1 << n):
        probe = QuantumCircuit(n + 1)
        for bit in range(n):
            if (x >> bit) & 1:
                probe.x(bit)
        probe.compose(oracle, inplace=True)
        state = Statevector.from_instruction(probe)
        ancilla_probabilities = state.probabilities([n])
        p_one = float(ancilla_probabilities[1])
        if abs(p_one - round(p_one)) > atol:
            raise ValueError(
                f"Oracle is not deterministic on x={format(x, f'0{n}b')}: "
                f"P(ancilla=1)={p_one:.6f}."
            )
        table.append((format(x, f"0{n}b"), int(round(p_one))))
    return table


def is_constant_or_balanced(table: Iterable[tuple[str, int]]) -> str:
    """Classify a Boolean truth table as ``constant`` or ``balanced``."""
    values = [value for _, value in table]
    if not values:
        raise ValueError("The truth table is empty.")
    if all(value == values[0] for value in values):
        return "constant"
    if sum(values) * 2 == len(values):
        return "balanced"
    raise ValueError("The function is neither constant nor balanced.")


def classical_dj_queries(n: int) -> int:
    """Worst-case deterministic classical queries for an N-bit promise problem."""
    if n < 1:
        raise ValueError("n must be at least 1.")
    return 2 ** (n - 1) + 1


def bell_circuit(measure: bool = True) -> QuantumCircuit:
    """Return a two-qubit Bell pair."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    if measure:
        circuit.measure_all()
    return circuit


def ghz_circuit(num_qubits: int = 3, measure: bool = True) -> QuantumCircuit:
    """Return an ``num_qubits``-qubit GHZ state."""
    if num_qubits < 2:
        raise ValueError("A GHZ state needs at least two qubits.")
    circuit = QuantumCircuit(num_qubits)
    circuit.h(0)
    for qubit in range(num_qubits - 1):
        circuit.cx(qubit, qubit + 1)
    if measure:
        circuit.measure_all()
    return circuit


def cnot_direction_pair() -> tuple[QuantumCircuit, QuantumCircuit]:
    """Return the direct CNOT and the H-sandwich version with reversed direction."""
    direct = QuantumCircuit(2)
    direct.cx(1, 0)

    flipped = QuantumCircuit(2)
    flipped.h([0, 1])
    flipped.cx(0, 1)
    flipped.h([0, 1])
    return direct, flipped


def cnot_direction_equivalent() -> bool:
    """Return whether the H-sandwich CNOT equals the reversed-direction CNOT."""
    direct, flipped = cnot_direction_pair()
    return Operator(direct).equiv(Operator(flipped))


def most_common(counts: dict[str, int], limit: int = 8) -> list[tuple[str, int]]:
    """Return the most common bitstrings, useful for noisy-hardware output."""
    return Counter(counts).most_common(limit)
