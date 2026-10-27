from itertools import product

import pytest

from classic_circuits.multiplier import bits_to_int, multiply_2x2_bits


def test_all_input_pairs_match_integer_multiplication():
    for a, b in product(range(4), repeat=2):
        a1, a0 = (a >> 1) & 1, a & 1
        b1, b0 = (b >> 1) & 1, b & 1
        assert bits_to_int(multiply_2x2_bits(a1, a0, b1, b0)) == a * b


def test_shared_carry_identity():
    for a1, a0, b1, b0 in product((0, 1), repeat=4):
        p0 = a0 & b0
        p1 = a0 & b1
        p2 = a1 & b0
        p3 = a1 & b1
        assert (p1 & p2) == (p0 & p3)


@pytest.mark.parametrize("inputs", [(-1, 0, 0, 1), (2, 0, 0, 1), (0, 0, 0, 0.0), (True, 0, 0, 1)])
def test_rejects_non_bits(inputs):
    with pytest.raises(ValueError):
        multiply_2x2_bits(*inputs)
