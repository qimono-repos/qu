import math

import pytest

from quantum_circuits.superposition import superposition_stats


def test_three_qubits():
    summands, amp, prob = superposition_stats(3)
    assert summands == 8
    assert amp == pytest.approx(1 / math.sqrt(8))
    assert prob == pytest.approx(1 / 8)


def test_four_qubits():
    summands, amp, prob = superposition_stats(4)
    assert summands == 16
    assert amp == pytest.approx(1 / 4)
    assert prob == pytest.approx(1 / 16)


@pytest.mark.parametrize("bad", [0, -1, 2.0, True])
def test_rejects_invalid_n(bad):
    with pytest.raises(ValueError):
        superposition_stats(bad)
