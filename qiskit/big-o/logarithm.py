#!/usr/bin/env python3
"""O(log n) — logarithmic time.

Each step throws away half of the remaining candidates. Classic
example: binary search on a sorted list. Doubling n adds only one
comparison.

This file is the second tile of the classical Big-O gallery. It does
not import the constant sibling. Quantum hook: a classical structured
search is O(log n); unstructured search is O(n) classically and
O(√n) with Grover.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class std:
    import math
    import pathlib


# Linear x so O(log n) looks like the familiar curve, not a ruler.
NS = [1, *range(100, 2001, 100)]  # 1, 100, 200, … 2000


def binary_search(sorted_items: list[int], target: int) -> tuple[int | None, int]:
    """Return (index or None, comparison count).

    Each loop iteration is one comparison against the midpoint.
    """
    lo = 0
    hi = len(sorted_items) - 1
    comparisons = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if sorted_items[mid] == target:
            return mid, comparisons
        if sorted_items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None, comparisons


def log2_steps(n: int) -> int:
    if n <= 1:
        return 1
    return std.math.ceil(std.math.log2(n))


def main() -> None:
    demo = list(range(16))
    idx, steps = binary_search(demo, 11)
    print("O(log n) demo — binary search\n")
    print(f"  haystack = {demo}")
    print(f"  find 11 → index {idx} after {steps} comparisons")
    print(f"  ceil(log2(16)) = {log2_steps(16)}")

    print("\nworst-case comparisons vs n  (O(1) overlaid)\n")
    print(f"{'n':>8}  {'O(1)':>8}  {'measured':>10}  {'ceil(log2 n)':>14}")
    ones: list[int] = []
    measured: list[int] = []
    theory: list[int] = []
    for n in NS:
        hay = list(range(n))
        # A value smaller than every element forces a full descent.
        _, cmp_count = binary_search(hay, -1)
        ones.append(1)
        measured.append(cmp_count)
        theory.append(log2_steps(n))
        print(f"{n:8d}  {1:8d}  {cmp_count:10d}  {log2_steps(n):14d}")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(NS, ones, "o-", label="O(1)  list[i]")
    ax.plot(NS, measured, "s--", label="binary search (measured)")
    ax.plot(NS, theory, "x:", label="ceil(log2 n)")
    ax.set_xlabel("n  (size of the input)")
    ax.set_ylabel("elementary steps")
    ax.set_title("O(1) vs O(log n) — measured binary search")
    ax.legend()
    ax.grid(True, which="both", linestyle=":")
    fig.tight_layout()
    out = std.pathlib.Path(__file__).with_name("logarithm-vs-constant.png")
    fig.savefig(out, dpi=120)
    print(f"\nwrote {out.name}  (gitignored)")


if __name__ == "__main__":
    main()
