# Q# workspace

Quantum programs in Microsoft's standalone Q# language.

## Modern standalone Q#

This workspace uses **modern standalone Q#** — no `.csproj` or C# host needed.
Each `.qs` file is self-contained with `import Std.*` namespaces and top-level
`operation` declarations.

### What was removed

The legacy files (`Main.qs`, `Program.qs`, `porgram.cs`, `qsharp.sln`) have been
removed. They used the old Q# SDK syntax (`namespace TrainingQsharp { ... }` with
`open Microsoft.Quantum.*` imports) and required a C# host project. Modern Q#
does not need any of that.

### Run a program

```bash
qsharp run main.qs
```

### Install Q# (pick one)

**Option A — Python package (recommended):**
```bash
pip install qsharp
```

**Option B — npm:**
```bash
npm install -g qsharp
```

**Option C — Standalone binary:**
Download from https://github.com/microsoft/qdk/releases

### Install .NET 10 SDK (for resource estimation / Azure Quantum)

> .NET 10 is currently **preview** (stable: November 2026).

**Flatpak (preferred):**
```bash
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.microsoft.dotnet.Extension.Sdk
```

**Microsoft install script:**
```bash
wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh
chmod +x dotnet-install.sh
./dotnet-install.sh --channel 10.0 --install-dir $HOME/.dotnet
```

## Project structure

```
qsharp/
├── main.qs                    # Hello World — random bit via superposition
├── teleportation.qs           # Quantum teleportation protocol
├── qsharp.csproj              # For resource estimation / Azure Quantum only
├── basic/                     # Fundamental quantum concepts
│   ├── computational-basis/
│   │   └── computational_basis.qs   # |0⟩ and |1⟩ states, measure, print
│   ├── statevectors/
│   │   └── statevectors.qs          # |+⟩, |−⟩ via H, DumpMachine()
│   ├── logic-gates/
│   │   └── logic_gates.qs           # X, Y, Z, H, S, T gates
│   ├── phase/
│   │   └── phase.qs                 # S, T, S†, T† phase changes
│   ├── superposition/
│   │   └── superposition.qs         # Hadamard + 10 repeated measurements
│   ├── bloch-sphere/
│   │   └── bloch_sphere.qs          # Rx, Ry, Rz rotations
│   ├── measurement/
│   │   └── measurement.qs           # Z-basis vs X-basis measurement
│   ├── tensor-products/
│   │   └── tensor_products.qs       # 2-qubit combined states
│   ├── controlled-gates/
│   │   └── controlled_gates.qs      # CNOT, CZ, CH
│   ├── entanglement/
│   │   └── entanglement.qs          # Bell states |Φ+⟩, |Φ−⟩, |Ψ+⟩
│   └── toffoli/
│       └── toffoli.qs               # CCX (Toffoli) gate, AND demo
└── algorithms/                # Quantum algorithms
    ├── oracle-basics/
    ├── phase-kickback/
    ├── deutsch-jozsa/
    ├── qft/
    ├── phase-estimation/
    ├── shor/
    └── grover/
└── optimization/              # Combinatorial optimisation
    ├── qaoa/
    └── tsp/
```

## Notes

- All circuits run on the **Q# simulator** — no Azure Quantum token needed.
- The `.csproj` file is kept for reference but is **not required** for modern
  standalone Q#. It is only needed for resource estimation or Azure Quantum
  submission.
- To target real Azure Quantum hardware, use the `qsharp` package's
  Azure Quantum submission API.
- Q# uses **big-endian** qubit ordering (qubit 0 is the leftmost bit).
