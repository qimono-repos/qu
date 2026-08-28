# Complex numbers in quantum computing

Every amplitude of a quantum state is a complex number. This page is the
shared reference for the Qiskit `basic/phase`, `basic/superposition`,
`algorithms/qft` topics and their equivalents in the other stacks.

## Definition

A complex number in rectangular form, with real part `a` and imaginary
part `b`:

```math
\begin{aligned}
z &= a + bi && a, b \in \mathbb{R}, \quad i^2 = -1 \\
\bar{z} &= a - bi && \text{complex conjugate} \\
|z| &= \sqrt{a^2 + b^2} && \text{modulus (magnitude, norm)}
\end{aligned}
```

The conjugate negates the imaginary part; the modulus is the distance from
the origin in the complex plane.

## Euler's formula (polar / phasor form)

```math
e^{i\theta} = \cos\theta + i\sin\theta
```

So any complex number can be written with a radius and an angle:

```math
z = r e^{i\theta}, \qquad r = |z|, \qquad \theta = \arg(z)
```

Multiplying two complex numbers *rotates and scales*:

```math
r_1 e^{i\theta_1} \cdot r_2 e^{i\theta_2} = r_1 r_2 e^{i(\theta_1 + \theta_2)}
```

Special values used constantly in QC:

```math
e^{i\pi} = -1, \qquad e^{i\pi/2} = i, \qquad e^{-i\pi/2} = -i, \qquad e^{-i\pi/4} = \tfrac{1-i}{\sqrt{2}}
```

## Powers of i

```math
i^0 = 1, \quad i^1 = i, \quad i^2 = -1, \quad i^3 = -i, \quad i^4 = 1
```

This is the backbone of the phase/`T`/`S` gates: applying the phase
`T = diag(1, e^{i\pi/4})` four times is identity (`T^4 = I`).

## Probability amplitudes

A single-qubit superposition has complex amplitudes:

```math
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle, \qquad \alpha, \beta \in \mathbb{C}
```

The **Born rule** turns amplitudes into probabilities:

```math
p(|0\rangle) = |\alpha|^2, \qquad p(|1\rangle) = |\beta|^2, \qquad |\alpha|^2 + |\beta|^2 = 1
```

Note `|z|^2 = z\bar{z}` — probabilities only ever involve the modulus
squared, which is why a state times a pure phase is identical physically:

```math
|\psi\rangle \equiv e^{i\theta}|\psi\rangle \qquad \text{(global phase, unobservable)}
```

Relative phase (a different phase *between* the two amplitudes) *is*
observable — that difference is exactly what the `S`/`T`/`P` gates create.

## In the stack folders

| Topic | The complex math at work |
|---|---|
| `qiskit/basic/phase` | S, T, P gates multiply `\|1⟩` by `e^{iθ}` |
| `qiskit/basic/superposition` | `1/\sqrt{2}` magnitudes, `±` relative phase |
| `qiskit/algorithms/qft` | roots of unity `e^{2\pi i xk / N}` |
| `qsharp/basic/phase` | Q# `Rz` / `T` angles in radians |

See also [`quantum-algebra.md`](quantum-algebra.md) for how complex
amplitudes interact with operators.