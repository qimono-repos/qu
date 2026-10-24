"""Acceptance tests for ``specs/week-4/qasm-check.spec.md``."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "qasm_check.py"

QASM2_HEADER = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n'


def write_qasm(tmp_path: Path, name: str, body: str) -> Path:
    path = tmp_path / name
    path.write_text(QASM2_HEADER + body, encoding="utf-8")
    return path


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_t1_bell_distribution(tmp_path: Path) -> None:
    path = write_qasm(
        tmp_path,
        "bell.qasm",
        "qreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q -> c;\n",
    )
    result = run(str(path), "--expect", "00:0.5,11:0.5")
    assert result.returncode == 0, result.stderr
    assert "PASS" in result.stdout
    assert "FAIL" not in result.stdout


def test_t2_bit_order(tmp_path: Path) -> None:
    path = write_qasm(
        tmp_path,
        "bit-order.qasm",
        "qreg q[2];\ncreg c[2];\nx q[0];\n"
        "measure q[0] -> c[0];\nmeasure q[1] -> c[1];\n",
    )
    result = run(str(path))
    assert result.returncode == 0, result.stderr
    assert re.search(r"^\s*01\s+1024", result.stdout, re.MULTILINE)
    assert not re.search(r"^\s*10\s+", result.stdout, re.MULTILINE)


def test_t3_relative_phase_becomes_measurable(tmp_path: Path) -> None:
    path = write_qasm(
        tmp_path,
        "phase.qasm",
        "qreg q[1];\ncreg c[1];\nh q[0];\nz q[0];\nh q[0];\n"
        "measure q[0] -> c[0];\n",
    )
    result = run(str(path), "--expect", "1:1.0")
    assert result.returncode == 0, result.stderr
    assert "PASS" in result.stdout


def test_t4_equiv_cnot_direction(tmp_path: Path) -> None:
    direct = write_qasm(tmp_path, "direct.qasm", "qreg q[2];\ncx q[1],q[0];\n")
    flipped = write_qasm(
        tmp_path,
        "flipped.qasm",
        "qreg q[2];\nh q[0];\nh q[1];\ncx q[0],q[1];\nh q[0];\nh q[1];\n",
    )
    result = run("equiv", str(direct), str(flipped))
    assert result.returncode == 0, result.stderr
    assert "equal up to global phase" in result.stdout


def test_t5_parse_error_reports_line(tmp_path: Path) -> None:
    path = write_qasm(
        tmp_path,
        "broken.qasm",
        "qreg q[1];\nnot_a_gate q[0];\n",
    )
    result = run(str(path))
    assert result.returncode == 2
    assert "error:" in result.stderr.lower()
    assert re.search(r":\d+,\d+:", result.stderr)


def test_t6_statevector_exact_forms(tmp_path: Path) -> None:
    path = write_qasm(tmp_path, "h.qasm", "qreg q[1];\nh q[0];\n")
    result = run(str(path), "--statevector")
    assert result.returncode == 0, result.stderr
    assert "1/√2" in result.stdout


def test_t7_same_seed_same_counts(tmp_path: Path) -> None:
    path = write_qasm(
        tmp_path,
        "bell.qasm",
        "qreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q -> c;\n",
    )
    first = run(str(path), "--shots", "512", "--seed", "7")
    second = run(str(path), "--shots", "512", "--seed", "7")
    assert first.returncode == 0
    assert second.returncode == 0
    assert first.stdout == second.stdout


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
