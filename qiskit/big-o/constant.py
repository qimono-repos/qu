#!/usr/bin/env python3
"""O(1) — constant time.

The work does not grow with the size of the input. Classic example:
read one slot of a list, or one key of a dict. Ten items or ten million,
the CPU does one address calculation and one load.

This file is the first tile of a classical Big-O gallery. It does not
import the logarithm sibling. Quantum hook: Deutsch–Jozsa is also one
query, independent of n — that is O(1) *oracle calls*, which is why
this plot is the baseline we will overlay on O(log n).
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


NS = [2**k for k in range(0, 17)]  # 1 … 65536


def list_get(items: list[int], index: int) -> int:
    """One array access. Cost does not depend on len(items)."""
    return items[index]


def dict_get(table: dict[int, str], key: int) -> str:
    """Average-case hash lookup: also O(1)."""
    return table[key]


def count_list_get(_n: int) -> int:
    """How many element reads? Always 1."""
    return 1


def log2_steps(n: int) -> int:
    """Closed form for binary-search comparisons (ceil log2 n), n>=1."""
    if n <= 1:
        return 1
    return math.ceil(math.log2(n))


def main() -> None:
    items = list(range(max(NS)))
    table = {i: f"v{i}" for i in items}

    print("O(1) demo — one list access and one dict access, any n\n")
    print(f"  list_get(items, 0)        = {list_get(items, 0)}")
    print(f"  list_get(items, 999)      = {list_get(items, 999)}")
    print(f"  dict_get(table, 42)       = {dict_get(table, 42)}")

    print("\nsteps vs n  (O(1) is flat; O(log n) is the next tile)\n")
    print(f"{'n':>8}  {'O(1) reads':>12}  {'O(log n) cmp':>12}")
    ones: list[int] = []
    logs: list[int] = []
    for n in NS:
        c1 = count_list_get(n)
        lg = log2_steps(n)
        ones.append(c1)
        logs.append(lg)
        print(f"{n:8d}  {c1:12d}  {lg:12d}")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(NS, ones, "o-", label="O(1)  list[i]")
    ax.plot(NS, logs, "s--", label="O(log n)  binary search")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("n  (log scale)")
    ax.set_ylabel("elementary steps")
    ax.set_title("Constant vs logarithmic growth")
    ax.legend()
    ax.grid(True, which="both", linestyle=":")
    fig.tight_layout()
    out = Path(__file__).with_name("constant-vs-log.png")
    fig.savefig(out, dpi=120)
    print(f"\nwrote {out.name}  (gitignored)")


if __name__ == "__main__":
    main()
