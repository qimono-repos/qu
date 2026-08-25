# Q# workspace

Quantum programs in Microsoft's standalone Q# language.

## Quick start

Modern Q# runs as a standalone compiler — no `.csproj` or C# host needed.

### Install Q# (pick one)

**Option A — Python package (recommended):**
```bash
pip install qsharp
```

**Option B — npm (if you prefer Node):**
```bash
npm install -g qsharp
```

**Option C — Standalone binary:**
Download from https://github.com/microsoft/qdk/releases

### Install .NET 10 SDK (for resource estimation / Azure Quantum)

> .NET 10 is currently **preview** (stable: November 2026).
> Use .NET 9 LTS if you need stability today.

**Flatpak (preferred):**
```bash
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.microsoft.dotnet.Extension.Sdk
```

**Microsoft install script (more reliable on Ubuntu):**
```bash
wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh
chmod +x dotnet-install.sh
./dotnet-install.sh --channel 10.0 --install-dir $HOME/.dotnet
```

### Run a program

```bash
qsharp run main.qs
# or
python -c "import qsharp; qsharp.reload(); from qsharp import Result; print(Result)"
```

## Files

| File | Description |
|---|---|
| `main.qs` | Hello World — random bit via superposition |
| `teleportation.qs` | Quantum teleportation protocol |
| `BellState_OmegaPlus.qs` | Bell state preparation |
| `Main.qs` | Legacy entry point (old SDK syntax) |
| `Program.qs` | Legacy C# host bridge |
| `porgram.cs` | Historical C# host (typo preserved) |

## Legacy files

`Main.qs`, `Program.qs`, `BellState_OmegaPlus.qs`, `MeasureOneQubit.qs`,
and `RandomUtils.qs` use the **old** Q# SDK syntax
(`Microsoft.Quantum.*` namespaces). They still compile with the legacy
SDK but are not idiomatic modern Q#. The newer files (`main.qs`,
`teleportation.qs`) use the modern `import Std.*` syntax.

## Notes

- All circuits run on the **Q# simulator** — no Azure Quantum token needed.
- The `.csproj` and `.sln` files are kept for reference but are not
  required for modern standalone Q#.
- To target real Azure Quantum hardware, use the `qsharp` package's
  Azure Quantum submission API.
