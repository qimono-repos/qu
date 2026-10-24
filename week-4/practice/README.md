# Week 4 practice

Put hand-written OpenQASM katas here, for example `practice/katas/k1.qasm`.

Rules from `specs/week-4/qasm-katas.spec.md`:

- Write every `.qasm` file yourself.
- Record the prediction before running the check.
- These are ungraded exercises, not the graded QASM block or lab.
- Do **not** commit graded lab solutions, quiz answers, or the four N=1
  Deutsch-Jozsa oracles before the lab is submitted.

Check a kata from the repository root:

```bash
uv run --project week-4 python week-4/qasm_check.py week-4/practice/katas/k1.qasm --expect "0:1.0"
```

The `week-4/qasm-check` wrapper does the same thing:

```bash
week-4/qasm-check week-4/practice/katas/k1.qasm --expect "0:1.0"
```
