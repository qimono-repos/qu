# Quantum algebra

The day-to-day bra-ket algebra of gate-model programming: superposition,
measurement, expectation values, rotation gates, and the identities that
power the algorithm topics. Complements [`linear-algebra.md`](linear-algebra.md)
and [`complex-numbers.md`](complex-numbers.md).

## The qubit and superposition

```math
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle, \qquad \alpha, \beta \in \mathbb{C}, \qquad |\alpha|^2 + |\beta|^2 = 1
```

Applied by the Hadamard gate:

```math
H|0\rangle = \frac{1}{\sqrt{2}}\big(|0\rangle + |1\rangle\big), \qquad
H|1\rangle = \frac{1}{\sqrt{2}}\big(|0\rangle - |1\rangle\big), \qquad
H^2 = I
```

## Measurement (Born rule + collapse)

```math
p(x) = |\langle x|\psi\rangle|^2, \qquad |\psi\rangle \;\xrightarrow{\text{meas } x}\; |x\rangle
```

The qubit collapses onto the computational-basis state that was observed.
Qiskit `basic/measurement` and `basic/bloch-sphere` explore this.

## Expectation values

For an observable `A` (Hermitian):

```math
\langle A \rangle = \langle\psi|A|\psi\rangle
```

For a Pauli observable this doubles as a graph of the Bloch vector:

| State | `⟨Z⟩` | `⟨X⟩` |
|---|---|---|
| `|0⟩` | `+1` | `0` |
| `|1⟩` | `-1` | `0` |
| `|+⟩` | `0` | `+1` |
| `|-⟩` | `0` | `-1` |

## Rotation gates (Pauli exponentiation)

The defining identity: exponentiating a Pauli gives a rotation.

```math
e^{-i\theta \sigma/2} = \cos\frac{\theta}{2}\, I - i \sin\frac{\theta}{2}\, \sigma
```

so

```math
R_x(\theta) = e^{-i\theta X/2}, \quad R_y(\theta) = e^{-i\theta Y/2}, \quad R_z(\theta) = e^{-i\theta Z/2}
```

Special case when `H` squares to identity (`H^2 = I` ⇒ `e^{-iθH} = I\cosθ - iH\sinθ`)
is the engine of QAOA/adiabatic evolution:

```math
e^{-i\beta C} = \cos\beta \cdot I - i \sin\beta \cdot C \qquad (C \text{ any Hermitian with } C^2 = I)
```

## Pauli algebra

```math
X^2 = Y^2 = Z^2 = I, \qquad XY = iZ, \quad YZ = iX, \quad ZX = iY, \qquad [X,Y] = 2iZ
```

`X` and `Z` **anti-commute**: `XZ = -ZX`. The Hadamard maps between them:

```math
HXH = Z, \qquad HZH = X, \qquad H = \frac{X + Z}{\sqrt{2}}
```

## Phase gates in matrix form

```math
S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}, \quad
T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}, \quad
T^2 = S, \quad S^2 = Z, \quad Z^2 = I
```

## Controlled gates

```math
CX_{c \to t} = |0\rangle\langle0| \otimes I + |1\rangle\langle1| \otimes X
```

`CX` is its own inverse and, up to Hadamards, the roles of control and
target swap:

```math
H^{\otimes2} \, CX_{c \to t} \, H^{\otimes2} = CX_{t \to c}
```

Toffoli generalizes `CX` to two controls (see `qiskit/basic/toffoli`).

The entanglement shortcut used by every Bell/EPR pair:

```math
|00\rangle \xrightarrow{H(q_0),\, CX(q_0 \to q_1)} \frac{|00\rangle + |11\rangle}{\sqrt{2}}
```

## Useful shortcut identities

```math
\begin{aligned}
\langle\psi|X|\psi\rangle + \langle\psi|Z|\psi\rangle &= \langle\psi|(X+Z)|\psi\rangle \\
H|\psi\rangle \quad\text{flips}\quad X &\leftrightarrow Z \\
e^{-i\theta Z/2}|0\rangle &= e^{-i\theta/2}|0\rangle, \qquad e^{-i\theta Z/2}|1\rangle = e^{+i\theta/2}|1\rangle \\
U^\dagger CU &= C' \qquad \text{(conjugated control, phase-kickback)}
\end{aligned}
```

## In the stack folders

| Topic | Algebra used |
|---|---|
| `qiskit/algorithms/phase-kickback` | `U` with eigenphase, controlled-`U` |
| `qiskit/algorithms/deutsch-jozsa` | `H^{\otimes n}` fanned across inputs |
| `qiskit/algorithms/qft` | tensor ids + rotations in the Fourier basis |
| `qiskit/optimization/qaoa` | `e^{-iγC} e^{-iβM}` alternating exponentials |
| `qiskit/simulation/vqe` | `⟨ψ(θ)|H|ψ(θ)⟩` minimization |

Suggested reading order: complex-numbers → linear-algebra → quantum-algebra,
then jump into any algorithm folder.