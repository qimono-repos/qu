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
