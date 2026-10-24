# specs/week-4

Spec-driven practice for the Week 4 hands-on part: OpenQASM (new) and Qiskit.

Why this exists: Albert writes the circuits by hand; tools are built from these specs (by a local LLM or anyone else) only to **check** his work, never to produce graded answers. Specs first, code second.

What belongs here: specs (`*.spec.md`) with requirements, interfaces and acceptance tests.
What does not: graded lab solutions, quiz answers, the four N=1 oracles before the lab is submitted.

| Spec | Purpose |
|---|---|
| `qasm-check.spec.md` | CLI that loads a hand-written `.qasm` file, simulates it and checks it against an expected result |
| `qasm-katas.spec.md` | Ungraded OpenQASM exercises with expected outcomes, to learn the syntax before the graded QASM block |

Time reference for the week: Paramaribo (UTC−3). Hard deadline Mon 2026-11-02 20:30 Paramaribo.
