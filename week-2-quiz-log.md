# Week 2 — Question Log

A dated record of practice/graded questions worked in session. Separate from week-2-experience.md (the timing + session log) so neither clobbers the other.

**Publication rule (2026-10-19):** this repository is public. Questions and options only; answers, correct options and Albert's selections are never published. Earlier versions of this file contained answers; they were removed from the current version on 2026-10-19 (git history not rewritten, by Albert's decision).

## Section 1 — What Makes a Good Qubit Modality?

### Q: Physical Requirements (graded practice, select all that apply) — completed, 1/1

Prompt: "David Divincenzo proposed five requirements for the physical realization of a quantum computer and two requirements for communicating quantum information. Identify which of the following are requirements for the physical realization of a quantum computer."

- Ability to measure the qubit state
- Ability to interconvert stationary and flying qubits
- Ability to robustly represent quantum information
- Ability to transmit flying qubits faithfully between two locations

Study note: the course numbers DiVincenzo's criteria differently from the 2000 paper; use the course numbering.

## Section 3 — Qubit Modalities (Electron and Nuclear Spins)

### Q1: NV Centers (graded practice, select all that apply) — completed, 1/1 on attempt 1 of 3 (2026-10-12 ~08:53 UTC−3)

Prompt: "The advantage(s) of qubits made using nitrogen vacancy centers, as presented in the video, are ___."

- They leverage advanced silicon fabrication technology
- They have the ability to interconvert stationary and flying qubits
- They have the ability to communicate quantum information
- They can be operated at room temperature

Lesson: when a question says "as presented in the video", the video's wording is the answer key. Watch for near-neighbor distractors: statements true of a different modality in the same video.

Study notes from the same video (transcript Q1M2V4a): NV centers "really shine as quantum sensors" of magnetic fields; main challenge is scalability. Quantum dots: silicon fab, small area, gate-voltage control; challenge = many gates per qubit, needs 3D integration. Phosphorus donors: silicon fab + very long coherence; challenge = ~10 nm dopant spacing, crosstalk, precise implantation. Nuclear spins: extremely long coherence, slow gates.

Note: the remaining Qubit Modalities questions (and the Qubit Robustness pair) were completed without being reviewed in this chat; only the platform scores are known (see scoreboard below).

## Section 4 — Case Study: Trapped-Ion Quantum Computers

### Measuring Ions — Q1 Ion States + Q2 Ion Measurement — completed, 2/2 (reported 2026-10-12 ~12:33 UTC−3)

Setup: energy-level diagram with an Auxiliary level; a Drive arrow up to Auxiliary and a wavy Detect arrow back down; two boxes, A and B, on the lower levels.

- Q1 "The atom in the diagram will be:" options: Dark / Bright.
- Q2 "Which of the below belongs in the 'A' box?" and "...in the 'B' box?" options: |1⟩ / (|0⟩ + |1⟩) / |0⟩ / (|0⟩ − |1⟩).

Study note: transcript Q1M2V7b, lines 58–73, covers ion readout (fluorescence, quantum non-demolition measurement, photon-count threshold).

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

## Section 5 — Case Study: Superconducting Qubit Quantum Computers

Study Concept Questions "Superconducting Qubits" and "Josephson Junction" (select all that apply, 3 attempts each, due 2026-11-02 20:30 −03). Loaded 2026-10-13 ~02:09 UTC−3 in no-spoiler mode; sources are transcripts Q1M2V11a and Q1M2V11b. Albert's picks and results not yet reported.

## Week 2 Quiz — 9.75/10 (97.5%)

Recorded 2026-10-14 ~00:10 UTC−3 from Albert's completion record (completion date given as Tuesday 2026-10-13). Questions were not reviewed in this chat.

- Q7: −0.25, partial credit on a select-all-that-apply. Cause not established (missed correct option, extra wrong option, or both). Open: ask the course team how multi-select partial credit is scored.
- Bloch sphere question solved by voice alone.
- Flag: the record says "19 questions"; the course page and score show 10.
