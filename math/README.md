# Math backbone

The shared mathematical reference for **every** framework in this repo
(Q#, Qiskit, Cirq, PennyLane, Braket, …). Topics live here instead of in
each stack folder so the algebra appears once and each
`README.md`/notebook can link to it.

## Files

| File | What it covers |
|---|---|
| [`complex-numbers.md`](complex-numbers.md) | complex numbers, Euler, phasors, probability amplitudes, global phase |
| [`linear-algebra.md`](linear-algebra.md) | vectors, inner/outer products, matrices, Hermitian/unitary, Paulis, tensor products |
| [`quantum-algebra.md`](quantum-algebra.md) | bra-ket algebra, measurement, expectation, rotation gates, identities |

## How to read these files

The formulas are LaTeX and render on GitHub and in VS Code (Markdown Math).
Follow the **GitHub matrix rule**: anything multiline — `\\` row breaks,
`\begin{pmatrix}`, `\begin{aligned}`, `\begin{bmatrix}` — **must** live in
a <code>```math</code> fenced block, not inside `$$`. Simple one-line
formulas are fine as `$...$` / `$$...$$`.

To render a formula as an **SVG figure** for `assets/` (e.g. `fig-002.svg`),
use matplotlib inside the Qiskit venv (it ships STIX/Computer-Modern fonts,
so no LaTeX install is needed):

```bash
cd qiskit
./run python media/bell_state.py --out ../assets/fig-001.svg
```

matplotlib mathtext supports fractions, sqrt, Greek, and sub/superscripts,
but **not** `\begin{pmatrix}`/`aligned` environments — hand-build matrices
with `np` arrays in code, or use `tectonic` (in the shared Guix manifest,
see [`manifest.scm`](../manifest.scm)) for full LaTeX:

```bash
guix shell -m manifest.scm
tectonic formula.tex            # -> formula.pdf
pandoc --pdf-engine=tectonic math/quantum-algebra.md -o algebra.pdf
```

## Notation conventions (whole repo)

- **Bra-ket**: kets are column vectors `|ψ⟩`, bras are dual row vectors
  `⟨φ|`, inner product `⟨φ|ψ⟩`.
- **Computational basis**: `|0⟩ = [1  0]ᵀ`, `|1⟩ = [0  1]ᵀ`; for n qubits
  basis states `|b_{n-1} … b_0⟩` with `b_k ∈ {0,1}`.
- **Little-endian (Qiskit)**: the printed bitstring orders **qubit 0 on the
  right**. `|01⟩` means qubit 0 = 1, qubit 1 = 0. Other frameworks print
  big-endian — always state the convention in snippets.
- **Units**: angles in radians. Phase gates use `θ`, rotation gates
  `R_x(θ) = e^{-iθX/2}`.
- **Global phase**: `|ψ⟩` and `e^{iθ}|ψ⟩` are the same physical state.
- **Normalization**: amplitudes satisfy `Σ_k |α_k|² = 1`.

## Cross-links from the stacks

- Qiskit `basic/` superposition, phase, entanglement ➡ math/quantum-algebra.md
- Qiskit `algorithms/` phase-kickback, qft, shor ➡ math/linear-algebra.md + math/quantum-algebra.md
- All frameworks' `README.md` may point here for the derivation behind a topic.