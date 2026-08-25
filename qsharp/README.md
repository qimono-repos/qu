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
│   ├── statevectors/
│   ├── logic-gates/
│   ├── phase/
│   ├── superposition/
│   ├── bloch-sphere/
│   ├── measurement/
│   ├── tensor-products/
│   ├── controlled-gates/
│   ├── entanglement/
│   └── toffoli/
└── algorithms/                # Quantum algorithms
    ├── oracle-basics/
    ├── phase-kickback/
    ├── deutsch-jozsa/
    ├── qft/
    ├── phase-estimation/
    ├── shor/
    └── grover/
```

## Notes

- All circuits run on the **Q# simulator** — no Azure Quantum token needed.
- The `.csproj` file is kept for reference but is **not required** for modern
  standalone Q#. It is only needed for resource estimation or Azure Quantum
  submission.
- To target real Azure Quantum hardware, use the `qsharp` package's
  Azure Quantum submission API.
- Q# uses **big-endian** qubit ordering (qubit 0 is the leftmost bit).
