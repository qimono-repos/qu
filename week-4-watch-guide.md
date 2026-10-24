# Week 4 Watch Guide
## MIT xPRO QCFx1 · Introduction to Quantum Computing
### Week 4: A Simple Quantum Algorithm in Practice (4–5 hrs)

Scope: **videos only.** What to catch in each Week 4 video so the binge is study, not background. The practice part of the week (OpenQASM, Composer, Qiskit, Deutsch-Jozsa lab) lives in `specs/week-4/` and in the week log.

Built from the course transcripts Q1M4V1 to Q1M4V5 (not committed, course material). Same publication rule as the other weeks: **no quiz or practice answers, no saved or submitted selections in this public repo.**

## Clock and plan

Time reference: **Paramaribo (America/Paramaribo, UTC−3, no DST).** Halifax falls back to UTC−4 on Sun 2026-11-01, so from that day Halifax and Paramaribo differ by one hour. Paramaribo wins.

| Milestone | Paramaribo | UTC |
|---|---|---|
| Week 4 opens | Sun 2026-10-25 21:00 | Mon 2026-10-26 00:00 |
| Videos + in-video questions (4 options each) done | Mon 2026-10-26, end of day | |
| QASM + Qiskit practice, DJ lab (N=1, N=3), real-device run | Tue 2026-10-27 to Sat 2026-10-31 | |
| Target: every graded item submitted | Sun 2026-11-01 | |
| **Hard deadline: course ends, forums lock** | **Mon 2026-11-02 20:30** | **Mon 2026-11-02 23:30** |

Optimistic graceful landing: Nov 2 is buffer only. Fallback chain if the network fails: home connection, phone hotspot, cybercafe.

Catch for Nov 2: the end of Course 1 (QCFx1) is the start of Course 2 (QCFx2). Course 1 stays the priority until the deadline; Course 2 starts only after Course 1 is closed.

## Graded items this week (from the course sidebar)

| Section | Estimate | Questions |
|---|---|---|
| Circuit Models | 10 min | 2 |
| The Deutsch-Jozsa Quantum Algorithm | 10 min | 1 |
| Quantum Software | 15 min | 1 |
| IBM QE: QASM | 40 min | 16 |
| Lab Practicum: IBM QE: Deutsch-Jozsa (N=1 data + 1 ancilla, N=3 data) | 2 h | |
| Week 4 Quiz | 30 min | 5 |
| Post-Assessment | 10 min | |

**One attempt per question.** Use Save, not Submit, until the section's videos and readings are done.

## V1 · Classical circuit model

- Three stages: **initialize → compute → measure.** Reset to zeros first ("not absolutely necessary" classically, included for comparison with the quantum model).
- Full adder example: inputs B1, B2, carry-in B3; outputs sum = B1+B2 mod 2 and carry-out, stored in B4, B5. 1+1 gives sum 0, carry 1.
- Classical gates like AND/XOR lose information: from the output you cannot recover the input. Keep this as the contrast with unitary (reversible) quantum gates.
- Controller layer: UI gives data + instruction set, controller sets bits, runs gates, measures, returns data.

## V2 · Quantum circuit model

- Same three stages. Qubits reset to |0⟩, then initialized.
- H on each qubit gives an equal superposition. Normalization: 1/√2 (1 qubit), 1/2 (2 qubits), 1/(2√2) = (1/√2)³ (3 qubits, 8 terms).
- Measurement projects onto the measurement basis: probability = |coefficient|², one classical bit per qubit.
- Measuring the bare equal superposition of 3 qubits: 1/8 for each outcome. A good algorithm uses interference to pile **all amplitude on the state that encodes the answer**, so the measurement gives it with probability 1.

## V3 · Deutsch-Jozsa (watch twice)

- Problem: f takes N bits, returns 0 or 1, and is promised to be **constant** or **balanced**. Decide which.
- Classical deterministic cost: 2^N/2 + 1 queries in the worst case. Quantum: 1 query.
- N=1 walk-through: data qubit starts |0⟩, ancilla (helper) starts |1⟩. H on both: data |+⟩, ancilla |−⟩.
- Oracle U_f: |x, y⟩ → |x, y ⊕ f(x)⟩. The captions write XOR as "x ord" and garble "y XOR f(x)". Read them as XOR.
- **Key step (~5:20):** with the ancilla in (|0⟩ − |1⟩)/√2, the XOR turns into a factor (−1)^f(x) that moves onto the data qubit. This is **phase kickback**; the video shows it without naming it. Check all four cases on paper, as the video asks.
- Final H on the data qubit converts that relative phase into a computational-basis outcome (interference). Measuring the data qubit tells constant from balanced; the ancilla ends in |1⟩.
- The video writes (−1)^f(x) as e^(−iπ f(x)). Same thing: e^(iπ) = e^(−iπ) = −1.
- Practice before reading the text unit: the four N=1 functions are f = 00, 11, 01, 10 (f(0) f(1)). Build each U_f using only X and CNOT. Write them yourself; do not commit them here before the lab is submitted.
- Note: the video calls the N=1 case (2 queries vs 1) "exponential". The speed-up only means something as N grows.

## V4a · Quantum software stack

Classical ↔ quantum tool analogies:

| Classical | Quantum |
|---|---|
| Schematic capture CAD | IBM Composer |
| Compiler (C++, VHDL/Verilog) | Quipper (Dalhousie), Q# → intermediate **QASM** |
| Assembler | Hardware mapping (Qiskit, superconducting): native gates + connectivity |
| SPICE (power, timing, correctness) | Quantum simulation: noise/error impact, gate fidelity under control waveforms |
| JTAG / boundary scan | **QCVV** (quantum characterization, verification, validation) |

- Three programming steps: **program generation** (hardware-agnostic) → **hardware-specific circuit mapping** → **hardware control and execution.**
- Three program-generation methods: schematic capture (Composer, knows hardware constraints), high-level languages (Quipper, Q#, Scaffold), problem-specific generation (Google OpenFermion, quantum chemistry).
- Control (classical, room temperature) and processing (quantum, millikelvin, in a dilution fridge) are separate systems, often physically apart.

## V4b · Control, QCVV, simulation

- Control hardware: arbitrary waveform generators, microwave sources, lasers. Software: Labber (commercial instruments); Qiskit (superconducting), ARTIQ (ion traps); many labs use homegrown stacks.
- **Randomized benchmarking:** long sequences of the target gate interleaved with random gates; gives **average fidelity**, mitigates state-prep and measurement error, but only **one metric.**
- **Gate set tomography:** full **process maps** (operator description of gate and error).
- Both need lots of data, so they are limited to small systems. Scalable QCVV is open research.
- QuTiP: Python, open quantum systems (qubits coupled to environment). Static modeling gives coherence time and noise sensitivity. Simulation also gives QEC logical error rates and their scaling with physical error rates, and sizes "supremacy" circuits on HPC simulators.

## V5 · IBM Q Experience, Composer, QASM

- Since 2016 the IBM Q Experience has given cloud access to real devices (video era: about 80,000 users, 3 million experiments).
- Device page: chip schematic, **connectivity graph** (limits which two-qubit gates you can apply), per-qubit and per-gate noise numbers, fridge at ~21 mK.
- Bell experiment: H on q0, CNOT q0→q1, measure both. Simulator first, then hardware. Roughly 50% `00`, 50% `11`; default ~1000 shots. Hardware shows extra outcomes from noise.
- QASM = quantum assembly, a **hardware-agnostic** circuit description language; data dependencies, **no explicit timings**. Composer generates QASM under the hood.
- Program structure: `include` the standard gate library → `qreg` (5 qubits) → `creg` → gates → `measure`.
- CNOT direction: on that chip, CNOT q2→q3 was not allowed, only q3→q2. Fix: **H on both qubits, CNOT, H on both** gives a CNOT with control and target swapped. Cost: more gates, more error.
- Era warning: the video is from about 2018. Today's Composer UI is different and the transpiler routes and flips CNOTs automatically. For questions, answer from the course framing. For the lab, expect a different UI.

## Prediction to settle after the binge

Do these two circuits give the same operator? Predict first, then run.

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

a = QuantumCircuit(2); a.cx(1, 0)                           # control q1, target q0
b = QuantumCircuit(2); b.h([0, 1]); b.cx(0, 1); b.h([0, 1])
print(Operator(a).equiv(Operator(b)))
```

Prediction: ______  Result: ______  Why: ______
