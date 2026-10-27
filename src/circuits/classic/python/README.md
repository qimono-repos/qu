# Classical circuits in Python

A dependency-light Python implementation of a 2-bit × 2-bit unsigned multiplier. The project is managed with `uv`; it does not need Qiskit.

## Run

From this directory:

```bash
uv run python -m classic_circuits.multiplier
uv run --extra test pytest
```

The exhaustive test checks all 16 input pairs against ordinary integer multiplication and checks the shared carry identity.

## Inputs and outputs

`multiply_2x2_bits(a1, a0, b1, b0)` accepts four bits and returns `(c3, c2, c1, c0)`. The corresponding integer product is `c3*8 + c2*4 + c1*2 + c0`.
