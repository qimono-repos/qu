#!/usr/bin/env python3
"""
Deutsch–Jozsa: classical vs quantum query cost analysis
Method only - no quiz answers.
"""

def classical_dj_worst_case(n, balanced_or_constant=True):
    """
    Under the promise (f is either constant or balanced),
    deterministic classical algorithm to distinguish with certainty:
    - If we ever see different outputs when checking, it's balanced.
    - To be certain it's constant, we must check until we see difference OR
      exhaust enough to rule out balanced. For balanced, outputs are split equally.
    Worst case: first 2^(n-1) evaluations all give same result -> must check
    1 more = 2^(n-1) + 1.
    """
    total = 2**n
    worst = (total // 2) + 1
    return worst

def dj_oracle_queries_constant():
    return 1  # quantum

def dj_oracle_queries_balanced():
    return 1  # quantum - always 1 query regardless

def main():
    print("Deutsch–Jozsa: query complexity (oracle queries)")
    print("=" * 50)
    for n in [1, 2, 3, 4, 5]:
        total = 2**n
        classical_worst = classical_dj_worst_case(n)
        print(f"n={n}, total={total:3d}, classical worst-case (det): {classical_worst:3d}, quantum: 1")
    print("=" * 50)
    print("Note: quantum gives exponential speedup in queries under promise")

if __name__ == '__main__':
    main()
