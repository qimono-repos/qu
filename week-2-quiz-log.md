# Week 2 — Question Log

A dated record of practice/graded questions worked in session. Separate from week-2-experience.md (the timing + session log) so neither clobbers the other.

## Section 1 — What Makes a Good Qubit Modality?

### Q: Physical Requirements (graded practice, select all that apply) — RESOLVED, CORRECT

Prompt: "Identify which of the following are requirements for the physical realization of a quantum computer."

- A. Ability to measure the qubit state — CORRECT (one of the five physical-realization requirements)
- B. Ability to interconvert stationary and flying qubits — NOT selected (communication requirement #6)
- C. Ability to robustly represent quantum information — CORRECT (physical-realization: coherence)
- D. Ability to transmit flying qubits faithfully — NOT selected (communication requirement #7)

Albert's answer: A and C. Saved. Result: correct.

Reasoning lock: DiVincenzo's seven split into five physical-realization + two communication (the quantum interconnect, #6 and #7). B and D are the communication pair and are the trap in this question. Uses COURSE numbering.

## Section 3 — Qubit Modalities (Electron and Nuclear Spins)

### Q1: NV Centers (graded practice, select all that apply) — RESOLVED, CORRECT (1/1, first attempt)

Prompt: "The advantage(s) of qubits made using nitrogen vacancy centers, as presented in the video, are ___."

- A. They leverage advanced silicon fabrication technology — NOT an NV advantage (video assigns this to quantum dots and phosphorus-doped silicon)
- B. They have the ability to interconvert stationary and flying qubits — CORRECT
- C. They have the ability to communicate quantum information — CORRECT
- D. They can be operated at room temperature — CORRECT (video: "albeit with some lower coherence")

Final answer: B, C, D. Submitted 2026-10-12 ~08:53 UTC−3. Result: 1/1 on attempt 1 of 3.

Failure caught before submit: Albert's first saved pick was C + D only (B omitted). Claude flagged that C without B is inconsistent (interconversion is the mechanism behind communication). Verified against transcript Q1M2V4a_REV_02_2026_FINAL-en.txt, lines 100–104, which names both "interconversion and communication" as NV advantages in one sentence.

Lesson: when a question says "as presented in the video", the video's wording is the answer key. Option A is a near-neighbor distractor: true of a different spin modality in the same video.

Quiz-likely details from the same video: NV centers "really shine as quantum sensors" of magnetic fields; main challenge is scalability (can't place high-coherence NVs precisely for large arrays). Quantum dots: silicon fab, small area, gate-voltage control; challenge = many gates per qubit, needs 3D integration. Phosphorus donors: silicon fab + very long coherence; challenge = ~10 nm dopant spacing, crosstalk, precise implantation. Nuclear spins: extremely long coherence, slow gates.

Note: the remaining Qubit Modalities questions (and the Qubit Robustness pair) were completed without being reviewed in this chat; only the platform scores are known (see scoreboard below).

## Section 4 — Case Study: Trapped-Ion Quantum Computers

### Measuring Ions — Q1 Ion States + Q2 Ion Measurement — RESOLVED, CORRECT (2/2)

Setup: energy-level diagram with an Auxiliary level; Drive arrow up from the bottom-left level to Auxiliary, wavy Detect arrow back down to the same level; separate level on the right labelled A; bottom-left level labelled B.

- Q1 "The atom in the diagram will be:" → **Bright** (it is shown cycling Drive → Detect).
- Q2 box A → **|0⟩** (level not coupled by the readout laser: dark).
- Q2 box B → **|1⟩** (the cycling level: bright).

Albert's picks matched before Claude's explanation. Result: 2/2, reported 2026-10-12 ~12:33 UTC−3.

Source: transcript Q1M2V7b lines 58–73: ion absorbs/re-emits "if it is measured in one state"; "zero state… the ion will be dark"; state is projected to 0 or 1 and stays (quantum non-demolition); photon-count threshold gives high-fidelity readout.
Distractor lesson: (|0⟩ ± |1⟩) options are wrong for both boxes. Levels in an energy diagram are basis states, and measurement projects; it never outputs a superposition.

Trapped-ion facts likely on the quiz (V5–V9): coherence ~10 min; single-qubit error ~1e-6 (microwave); two-qubit fidelity 99.9%; two-qubit gates via shared vibrational mode ("quantum bus"); ~500× (1q) / ~1000× (2q) slower than superconducting, similar 2q fidelity; larger connectivity may offset slow speed; surface traps on silicon, CMOS-compatible (DACs, APDs, integrated photonics); shuttling "quite unique to the ion qubit modality"; challenge = scaling from 1–10 ions to thousands–millions without room-sized bulk optics.

Stoplight chart (V5): NV centers yellow on initialization (laser can ionize the defect); neutral-atom measurement very slow; doped silicon has no reported 2q gate fidelity; neutral atoms and Si/Ge 2q fidelity ~80%; Si/Ge and doped Si yellow on scalability (wire density, needs 3D integration); no published D6/D7 work for Si/Ge or doped Si.

## Scoreboard snapshot — 2026-10-12 ~12:33 UTC−3 (from Progress page screenshot)

| Section | Score |
|---|---|
| What Makes a Good Qubit Modality? | 1/1 |
| Qubit Robustness | 2/2 |
| Qubit Modalities | 5/5 |
| Case Study: Trapped-Ion | 2/2 |
| Case Study: Superconducting | 0/2 (not started) |
| Week 2 Quiz | 0/10 (not started) |

Remaining: 2 superconducting questions + 10-question quiz. Target: wrap by 20:55 UTC−3 on 2026-10-12 (inside 24 h of the 21:00 Sunday start).
