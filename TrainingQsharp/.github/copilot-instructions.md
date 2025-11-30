<!-- Copilot instructions for the TrainingQsharp repo -->
# TrainingQsharp — Copilot Instructions

This file contains concise, actionable guidance for AI coding assistants working on this repository.

1. Big picture
- Project type: a small Q# application whose operations live in `.qs` files and compile into a .NET executable (`TrainingQsharp.csproj`).
- Entrypoint: `Program.qs` contains an `@EntryPoint()` operation (`HelloQuantumWorld`) executed by `dotnet run`.
- Generated artifacts: Q# compilation emits generated C# under `qsharp/src/` (e.g. `EntryPoint.g.Main.cs`, `Program.g.cs`). Do not edit generated files — change the `.qs` sources.

2. Where to look (examples)
- `Program.qs` — entry operation (`@EntryPoint()`).
- `Main.qs` — sample top-level operation `MainMeasure`.
- `RandomUtils.qs` — random number generation pattern (bit sampling, `ResultArrayAsInt`, recursive retry).
- `MeasureOneQubit.qs` — minimal qubit allocate->measure->reset example.
- `TrainingQsharp.csproj` — MS Quantum SDK and target framework (`Microsoft.Quantum.Sdk`, `net6.0`).

3. Build & run (developer workflows)
- Build: `dotnet build` from the repository root.
- Run entrypoint: `dotnet run` (or `dotnet run -c Debug`). The `@EntryPoint()` operation runs automatically.
- Debugging: attach a .NET debugger to the produced `TrainingQsharp.dll` under `bin/Debug/net6.0/` (the repo's dev environment already uses `vsdbg`).

4. Project-specific patterns and conventions
- File-level namespaces: operations are declared at file scope inside `namespace TrainingQsharp` — follow this when adding files.
- Random sampling pattern: `RandomUtils.qs` builds `bits` with `GenerateRandomBit()`, converts with `ResultArrayAsInt(bits)` and retries via recursion when sample > max. Example:

  - `let sample = ResultArrayAsInt(bits);`
  - `return sample > max ? GenerateRandomNumberInRange(max) | sample;`

- Qubit lifecycle: always `Reset` qubits before release (`Reset(q)` used in `MeasureOneQubit.qs` and `GenerateRandomBit()`). Avoid leaving qubits in a non-zero state.
- Logging: use `Message(...)` for simple run-time diagnostics (used in `Program.qs` and others).

5. Integration points & artifacts
- `qsharp/src/` contains generated C# shims — used at build/run time.
- `bin/` contains compiled outputs for multiple TFMs (`net6.0`, `net9.0`), language resources, and native runtimes under `runtimes/`.

6. Working with tests / missing items
- There are no test projects detected. If adding tests, prefer placing them in a separate test project and use `dotnet test`.

7. Editing guidance for AI agents
- Edit only `.qs` source files for Q# behavior changes. Do not modify generated files under `qsharp/src/`.
- Preserve existing idioms: qubit Reset, Message logging, and the recursive random-sampling retry.
- If adding new Q# files, follow the existing namespace (`TrainingQsharp`) and add a small example operation; update `Program.qs` only if you want to change the entry operation.

If anything here is unclear or you'd like different details (CI, target runtimes, or example run args), tell me what to expand and I'll update this file.
