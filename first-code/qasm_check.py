#!/usr/bin/env python3
"""qasm-check: simulate and check a hand-written OpenQASM file.

This implements the checker described in ``specs/week-4/qasm-check.spec.md``.
It never generates circuits or suggests fixes. It only loads, simulates, draws,
and checks what the learner wrote.

Examples:
    python qasm_check.py bell.qasm --draw
    python qasm_check.py bell.qasm --expect "00:0.5,11:0.5"
    python qasm_check.py bell.qasm --statevector
    python qasm_check.py equiv a.qasm b.qasm
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import qiskit
from qiskit import QuantumCircuit, qasm2, qasm3
from qiskit.quantum_info import Operator, Statevector


BIT_ORDER_REMINDER = (
    "Bit order: Qiskit prints c[n-1] on the left and c[0] on the right. "
    "A measurement of q[0] into c[0] therefore appears on the right."
)


class QasmCheckError(Exception):
    """A user-facing parse or input error."""


def load_circuit(path: Path, use_qasm3: bool = False) -> QuantumCircuit:
    """Load an OpenQASM 2 or OpenQASM 3 file, preserving parser messages."""
    text = path.read_text(encoding="utf-8")
    try:
        if use_qasm3:
            return qasm3.loads(text)
        return qasm2.loads(text)
    except Exception as exc:  # parser exceptions differ between QASM versions
        raise QasmCheckError(f"{type(exc).__name__}: {exc}") from exc


def ensure_measured(circuit: QuantumCircuit) -> QuantumCircuit:
    """Add a full measurement when a file has none, so counts are meaningful."""
    if circuit.num_clbits == 0:
        measured = circuit.copy()
        measured.measure_all()
        print("Note: the file had no measurement, so measure_all() was added.")
        return measured
    return circuit


def clean_for_unitary(circuit: QuantumCircuit) -> QuantumCircuit:
    """Return a copy without final measurements."""
    clean = circuit.copy()
    clean.remove_final_measurements(inplace=True)
    return clean


def get_counts(
    circuit: QuantumCircuit, shots: int, seed: int
) -> tuple[dict[str, int], str]:
    """Return counts and the simulator name that produced them."""
    try:
        from qiskit_aer import AerSimulator

        simulator = AerSimulator()
        result = simulator.run(
            circuit, shots=shots, seed_simulator=seed
        ).result()
        return dict(result.get_counts()), "AerSimulator"
    except ImportError:
        from qiskit.primitives import StatevectorSampler

        result = StatevectorSampler().run([circuit], shots=shots).result()
        data = result[0].data
        for name in ("meas", "measure", "c"):
            register = getattr(data, name, None)
            if register is not None and hasattr(register, "get_counts"):
                return dict(register.get_counts()), "StatevectorSampler"
        raise QasmCheckError(
            "No measurement data was produced. Add measurements to the circuit."
        )


def format_amplitude(amplitude: complex, atol: float = 1e-9) -> str:
    """Format common statevector amplitudes as exact-looking strings."""
    amplitude = complex(amplitude)
    if abs(amplitude) <= atol:
        return "0"

    magnitude = abs(amplitude)
    phase = 0.0 if magnitude == 0 else math.atan2(amplitude.imag, amplitude.real)
    exact_table = (
        (1.0, "1"),
        (0.5, "1/2"),
        (0.25, "1/4"),
        (1 / math.sqrt(2), "1/√2"),
        (1 / (2 * math.sqrt(2)), "1/(2√2)"),
        (math.sqrt(2) / 2, "1/√2"),
        (math.sqrt(2) / 4, "1/(2√2)"),
    )
    label = None
    for exact, text in exact_table:
        if abs(magnitude - exact) <= atol:
            label = text
            break
    if label is not None:
        if abs(phase) <= atol:
            return label
        if abs(abs(phase) - math.pi) <= atol:
            return f"-{label}"
        if abs(phase - math.pi / 2) <= atol:
            return f"i·{label}"
        if abs(phase + math.pi / 2) <= atol:
            return f"-i·{label}"

    if abs(amplitude.imag) <= atol:
        return f"{amplitude.real:.4f}"
    if abs(amplitude.real) <= atol:
        return f"{amplitude.imag:+.4f}i"
    return f"{amplitude.real:.4f}{amplitude.imag:+.4f}i"


def print_statevector(circuit: QuantumCircuit) -> None:
    """Print exact-looking amplitudes for the circuit's non-zero basis states."""
    clean = clean_for_unitary(circuit)
    state = Statevector.from_instruction(clean)
    print(f"{'bitstring':>10}  {'amplitude':>14}")
    print("-" * 28)
    for index, amplitude in enumerate(state.data):
        if abs(amplitude) <= 1e-9:
            continue
        bitstring = format(index, f"0{clean.num_qubits}b")
        print(f"{bitstring:>10}  {format_amplitude(amplitude):>14}")


def parse_expectations(text: str) -> dict[str, float]:
    """Parse ``"00:0.5,11:0.5"`` into a bitstring-to-probability mapping."""
    expectations: dict[str, float] = {}
    for chunk in text.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" not in chunk:
            raise QasmCheckError(
                f"Expected the form BITSTRING:PROBABILITY, got {chunk!r}."
            )
        bitstring, probability_text = chunk.split(":", 1)
        bitstring = bitstring.strip()
        if not bitstring or any(bit not in "01" for bit in bitstring):
            raise QasmCheckError(f"Invalid bitstring {bitstring!r} in --expect.")
        try:
            probability = float(probability_text)
        except ValueError as exc:
            raise QasmCheckError(
                f"Invalid probability {probability_text!r} in --expect."
            ) from exc
        if not 0.0 <= probability <= 1.0:
            raise QasmCheckError("Expected probabilities must be between 0 and 1.")
        expectations[bitstring] = probability
    if not expectations:
        raise QasmCheckError("--expect did not contain any bitstring:probability pair.")
    return expectations


def check_expectations(
    counts: dict[str, int],
    shots: int,
    expectations: dict[str, float],
    num_clbits: int,
) -> bool:
    """Print PASS/FAIL per expected outcome and return the overall result."""
    all_passed = True
    for bitstring, expected in expectations.items():
        if len(bitstring) != num_clbits:
            raise QasmCheckError(
                f"Expected bitstring {bitstring!r} has {len(bitstring)} bits, "
                f"but the circuit has {num_clbits} classical bits."
            )
        measured = counts.get(bitstring, 0) / shots
        if expected in (0.0, 1.0):
            passed = measured == expected
        else:
            tolerance = 3 * math.sqrt(expected * (1 - expected) / shots)
            passed = abs(measured - expected) <= tolerance
        all_passed = all_passed and passed
        print(
            f"  {bitstring}: expected {expected:.6f}, measured {measured:.6f} "
            f"[{'PASS' if passed else 'FAIL'}]"
        )
    return all_passed


def report_counts(counts: dict[str, int], shots: int) -> None:
    """Print counts sorted by bitstring, with probabilities."""
    print(f"{'bitstring':>10}  {'count':>7}  {'probability':>11}")
    print("-" * 33)
    for bitstring in sorted(counts):
        count = counts[bitstring]
        print(f"{bitstring:>10}  {count:>7}  {count / shots:>11.6f}")


def run_check(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    print(f"Qiskit version: {qiskit.__version__}")
    print(f"File: {path}")
    try:
        circuit = load_circuit(path, use_qasm3=args.qasm3)
        print(
            f"Qubits: {circuit.num_qubits}  Classical bits: {circuit.num_clbits}"
        )

        if args.draw:
            print()
            print(circuit.draw(output="text"))

        if args.statevector:
            print()
            print("Statevector (final measurements removed):")
            print_statevector(circuit)
            print()
            print(BIT_ORDER_REMINDER)
            return 0

        measured = ensure_measured(circuit)
        counts, simulator = get_counts(measured, shots=args.shots, seed=args.seed)
        print(f"Simulator: {simulator}  Shots: {args.shots}  Seed: {args.seed}")
        print()
        report_counts(counts, args.shots)

        if args.expect:
            expectations = parse_expectations(args.expect)
            print()
            print("Expectation check:")
            passed = check_expectations(
                counts, args.shots, expectations, measured.num_clbits
            )
            print()
            print(BIT_ORDER_REMINDER)
            return 0 if passed else 1

        print()
        print(BIT_ORDER_REMINDER)
        return 0
    except QasmCheckError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def run_equiv(first: str, second: str, use_qasm3: bool) -> int:
    print(f"Qiskit version: {qiskit.__version__}")
    try:
        first_circuit = load_circuit(Path(first), use_qasm3=use_qasm3)
        second_circuit = load_circuit(Path(second), use_qasm3=use_qasm3)
    except QasmCheckError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    first_unitary = Operator(clean_for_unitary(first_circuit))
    second_unitary = Operator(clean_for_unitary(second_circuit))
    equivalent = first_unitary.equiv(second_unitary)
    print(f"Comparing: {first}  vs  {second}")
    print("Unitaries are equal up to global phase." if equivalent else "Unitaries differ.")
    return 0 if equivalent else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Simulate and check a hand-written OpenQASM file. "
            "This tool is a checker, not a circuit generator."
        )
    )
    parser.add_argument("file", help="OpenQASM 2.0 file (or use --qasm3)")
    parser.add_argument(
        "--expect",
        metavar="DIST",
        help='Expected distribution, e.g. "00:0.5,11:0.5" or "1:1.0".',
    )
    parser.add_argument(
        "--shots", type=int, default=1024, help="Number of shots (default: 1024)."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Aer simulator seed (default: 42).",
    )
    parser.add_argument(
        "--statevector",
        action="store_true",
        help="Print the exact statevector with final measurements removed.",
    )
    parser.add_argument(
        "--draw", action="store_true", help="Print the text circuit diagram."
    )
    parser.add_argument(
        "--qasm3", action="store_true", help="Parse the file as OpenQASM 3."
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "equiv":
        if len(argv) != 3:
            print(
                "usage: qasm-check equiv A.qasm B.qasm [--qasm3]",
                file=sys.stderr,
            )
            return 2
        use_qasm3 = "--qasm3" in argv[1:]
        files = [item for item in argv[1:] if item != "--qasm3"]
        if len(files) != 2:
            print(
                "usage: qasm-check equiv A.qasm B.qasm [--qasm3]",
                file=sys.stderr,
            )
            return 2
        return run_equiv(files[0], files[1], use_qasm3)

    parser = build_parser()
    args = parser.parse_args(argv)
    if args.shots < 1:
        parser.error("--shots must be at least 1")
    return run_check(args)


if __name__ == "__main__":
    raise SystemExit(main())
