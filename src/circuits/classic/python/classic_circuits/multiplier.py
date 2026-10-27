"""A 2-bit by 2-bit unsigned multiplier expressed as Boolean gates."""


def _require_bit(name: str, value: int) -> None:
    if type(value) is not int or value not in (0, 1):
        raise ValueError(f"{name} must be the integer 0 or 1; got {value!r}")


def multiply_2x2_bits(a1: int, a0: int, b1: int, b0: int) -> tuple[int, int, int, int]:
    """Return product bits (c3, c2, c1, c0) for inputs a1,a0 and b1,b0."""
    for name, value in (("a1", a1), ("a0", a0), ("b1", b1), ("b0", b0)):
        _require_bit(name, value)

    # Partial products: four AND gates.
    p0 = a0 & b0
    p1 = a0 & b1
    p2 = a1 & b0
    p3 = a1 & b1

    # Shared product/carry term: fifth AND gate.
    p4 = p0 & p3

    # Output bits: two XOR gates, plus wires.
    c0 = p0
    c1 = p1 ^ p2
    c2 = p4 ^ p3
    c3 = p4
    return (c3, c2, c1, c0)


def bits_to_int(bits: tuple[int, int, int, int]) -> int:
    """Interpret four bits in c3,c2,c1,c0 order as an unsigned integer."""
    c3, c2, c1, c0 = bits
    return (c3 << 3) | (c2 << 2) | (c1 << 1) | c0


def main() -> None:
    print("2-bit × 2-bit classical multiplier")
    print(" a  b | product | circuit output")
    for a in range(4):
        for b in range(4):
            a1, a0 = (a >> 1) & 1, a & 1
            b1, b0 = (b >> 1) & 1, b & 1
            bits = multiply_2x2_bits(a1, a0, b1, b0)
            product = bits_to_int(bits)
            assert product == a * b, (a, b, product, a * b)
            print(f" {a}  {b} |    {product:2}    |     {''.join(map(str, bits))}")
    print("PASS: all 16 input pairs match integer multiplication.")


if __name__ == "__main__":
    main()
