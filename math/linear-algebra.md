# Linear algebra for quantum computing

The mathematical backbone of gate-model QC: states are vectors, gates are
matrices. Shared reference for `qiskit/basic/*`, `qiskit/algorithms/*`,
and the equivalent topics in every other gate-model stack.

## Vectors and duals

A quantum state is a **unit vector** in a complex Hilbert space
`\mathbb{C}^{2^n}` for `n` qubits. Column (ket) and row (dual/bra):

```math
|\psi\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}, \qquad
\langle\psi| = |\psi\rangle^\dagger = \begin{pmatrix} \bar{\alpha} & \bar{\beta} \end{pmatrix}
```

`†` is the **dagger**: transpose **and** complex-conjugate.

## Inner and outer products

The inner product of two kets contracts a bra with a ket:

```math
\langle\phi|\psi\rangle = \sum_k \bar{\phi}_k \psi_k, \qquad
\langle\psi|\psi\rangle = 1 \quad \text{(normalization)}
```

The outer product builds a **matrix** from a ket and a bra:

```math
|\psi\rangle\langle\psi| = \begin{pmatrix}
  \alpha\bar{\alpha} & \alpha\bar{\beta} \\
  \beta\bar{\alpha} & \beta\bar{\beta}
\end{pmatrix}
\qquad \text{rank-1 projector}
```

## Matrices: what gates are

A gate is a complex matrix that maps state → state. The two classes that
matter:

| Property | Definition | Meaning |
|---|---|---|
| **Hermitian** | `A† = A` | real eigenvalues → **observables** |
| **Unitary** | `U†U = UU† = I` | norm-preserving → **gates** |

The dagger reverses order in products: `(AB)† = B†A†`.

### Pauli matrices

The four basis operators on one qubit, listed little-endian (qubit 0 right):

```math
I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad
X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad
Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad
Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}
```

Each is **both Hermitian and unitary**, squares to identity, and the set
`{X, Y, Z}` together with `I` spans all single-qubit observables.

## Eigenvalues and spectral decomposition

For a normal matrix, the projector form (identity resolution):

```math
A = \sum_k \lambda_k |\lambda_k\rangle\langle\lambda_k|, \qquad
\sum_k |\lambda_k\rangle\langle\lambda_k| = I
```

`Z` has `+1` on `|0⟩` and `-1` on `|1⟩`; `X` has `+1` on `|+⟩`, `-1` on
`|-⟩`. Measuring = sampling one eigenvalue weighted by `|\langle\lambda_k|\psi\rangle|^2`.

## Tensor product (Kronecker product)

Composing independent systems. For a `2×2` matrix `A`, the Kronecker
product bloats it with a repeating block structure:

```math
A \otimes B = \begin{pmatrix}
  a_{11}B & a_{12}B \\
  a_{21}B & a_{22}B
\end{pmatrix},
\qquad
|a\rangle \otimes |b\rangle = |ab\rangle
```

Consequences that shape every nibble in this repo:

- `n` qubits → state space of dimension `2^n` (exponential — the whole point).
- The tensor is **not** commutative in general: `A⊗B ≠ B⊗A` for the
  operators on *different* qubits.
- Ordering is convention, but Qiskit labels qubits little-endian, so reorder
  blocks accordingly when reading printouts.

### Worked example: CX as a 4×4 matrix

`CX` (CNOT) with control qubit 1, target qubit 0:

```math
CX_{1 \to 0} = |0\rangle\langle0| \otimes I + |1\rangle\langle1| \otimes X
= \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}
```

## In the stack folders

| Topic | The algebra at work |
|---|---|
| `qiskit/basic/tensor-products` | `H⊗I`, multi-qubit circuit matrices |
| `qiskit/basic/controlled-gates`, `toffoli` | block-structure matrices |
| `qiskit/algorithms/qft` | `F = (1/\sqrt{N}) Σ ω^{xy}\|x⟩⟨y\|`, diagonal in Fourier basis |
| `qiskit/algorithms/phase-estimation`, `shor` | eigenphases of unitary `U` |
| `qiskit/optimization/qaoa` | mixer/cost as `e^{-iβH}`, `e^{-iγC}` |

See [`quantum-algebra.md`](quantum-algebra.md) for the bra-ket identities
built on top of this.