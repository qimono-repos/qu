# Week 2 Experience Log
## MIT xPRO QCFx1 · Introduction to Quantum Computing

This file records the study workflow, timing conventions, and session experience for Week 2 so that another LLM can continue the work interchangeably.

## Objective and operating mode

The learner has already binge-watched the Week 2 instructional material. This session is for theoretical discussion, conceptual consolidation, and careful analysis of the actual MIT xPRO course questions. Mathematics should remain light in this conversation; dedicated conversations handle mathematical practice and forums.

The goal is reliable understanding and independently verified correctness, not simply completing the platform's estimated hours. Preserve the course's terminology, order, exact question wording, and source context. Do not invent course content or answer options.

## Canonical module sequence

From the supplied course screenshot:

1. **Week 2: Leading Qubit Modalities (4–5 hrs)**
2. What Makes a Good Qubit Modality? — 15 min, 1 question.
3. Qubit Robustness — 25 min, 2 questions:
   - Qubit Coherence and Gate Time
   - Gate Fidelity
   - Discussion: Randomized Benchmarking and Gate Fidelity
4. Qubit Modalities — 35 min, 5 questions.
5. Case Study: Trapped-Ion Quantum Computers — 40 min, 2 questions.
6. Case Study: Superconducting Qubit Quantum Computers — 45 min, 2 questions.
7. Week 2 Quiz — 30 min, 10 questions.
8. Key Images — 3 min.

The displayed lesson durations sum to 163 minutes. Including the 30-minute quiz gives 193 minutes (3 h 13 min), excluding any other discussion and review. MIT xPRO/edX's displayed 4–5 hour estimate is a planning estimate, not a measurement of actual time to mastery.

## Three-clock timing system

Maintain three different measures:

- **Course clock:** published estimates and actual video/activity durations when source-supported.
- **Study clock:** actual conceptual discussion, question analysis, retrieval practice, and consolidation. Distinguish wall-clock time from focused time whenever the available data supports it.
- **Human clock:** breaks, coffee, meals, recovery, fatigue, and interruptions. These are part of the learning system, not failures.

The learner expects a planned coffee/recovery break approximately every three hours of sustained work. This is a practical preference, not a rigid scientific rule; adapt to actual fatigue and circumstances. The learner uses the four-hour Le Mans racing stint as an analogy for disciplined endurance and recovery. Do not assume studying and racing have identical optimal work intervals.

Never invent focused-study duration, break duration, timestamps, or elapsed time. If only a start time is known, report only what is supported. At session closure, record the end time if available, elapsed time, known focused time, confirmed breaks, topics covered, questions reviewed, misconceptions, and unresolved issues.

## Timezone convention and starting reference

The course uses GMT/UTC as its shared time reference.

Learner-provided start reference for this Week 2 session:
- Date: 2026-10-11 local date.
- Start time: 21:00 in the learner's stated Halifax/Paramaribo timezone reference.
- Stated UTC offset: UTC−3.
- Equivalent UTC time: 2026-10-12 00:00 UTC.

The learner later reported the current time as **09:38 Halifax/Paramaribo**. The date was not explicitly restated in that message. Do not calculate elapsed session time from the 21:00 start until the date and whether this is the same uninterrupted session can be established. If the 09:38 reading refers to the following local morning, it is 12 hours 38 minutes after 21:00 by wall clock, but that is not evidence of 12 hours 38 minutes of studying. Confirm the date and interpret the continuity carefully before logging a precise interval.

> **Resolved (Claude, see Session Log):** "09:38" = **21:38 the same evening** (2026-10-11 local / 2026-10-12 00:38 UTC). Evidence: the commit creating this file (218a777) is stamped 2026-10-12T00:39:35Z, i.e. 21:39 local — one minute after the reported reading. The learner also confirmed a continuous session starting at 21:00.

Use date-specific timezone offsets for all future conversions. Halifax and Paramaribo should not be treated as interchangeable year-round without verifying the date-specific offset. In this stated session reference, the learner explicitly specified UTC−3.

## Required question-defense protocol

Use Qimono's Fatal-Error Defense Mode on every course question:

1. **Source lock:** read the exact original wording and all visible answer choices.
2. **Object lock:** identify the precise subject being asked about.
3. **Target lock:** identify the exact property or relationship requested.
4. **Candidate quarantine:** treat the learner's answer as a hypothesis, not as evidence.
5. **Independent reasoning:** solve without relying on the learner's conclusion.
6. **Distractor analysis:** check whether a tempting option is true of a neighboring concept but wrong for the object actually named.
7. **Source reconciliation:** compare the result with the actual course material and its qualifications.
8. **Explain the verdict:** state why the correct answer is supported, why the strongest distractor is tempting, and what distinction resolves the question.
9. **Track recurring failures:** test the underlying misconception with new questions rather than merely repeating the original.

Do not optimize for agreement. Optimize for independently verified correctness. The Week 1 post-mortem recorded a failure in which a question about a classical bit was answered through a qubit/superposition interpretation. Never let neighboring concepts overwrite the question's literal scope.

## Teaching style and scope

Start with intuition, then refine the definition. Explain why a concept matters and how it differs from adjacent concepts. The learner is an experienced software developer and prefers direct, technically precise explanations, concrete examples, and occasional nerd humor. Correct mistakes plainly and explain the mental model that produced them.

Keep this conversation primarily theoretical with low mathematics. Avoid unnecessary derivations and unrelated Qiskit exercises. Do not jump ahead to Deutsch–Jozsa or later modules unless required by the Week 2 source or requested by the learner.

Distinguish explicitly between:
- facts supported by the supplied MIT xPRO material,
- supplementary general quantum-computing knowledge,
- inference,
- and unresolved uncertainty.

Never claim to have inspected source material that was not actually available or read.

## Session progress at file creation

- The learner reported that all Week 2 instructional material had already been binge-watched.
- The Week 2 module structure was captured from a course screenshot.
- The session's main objective and three-clock timing approach were established.
- The course footer screenshot indicates that the course is powered by edX; platform time estimates should be interpreted accordingly.
- No individual Week 2 course question has yet been analyzed in this conversation.
- No Week 2 quiz result is recorded.
- Do not claim any topic or question is mastered or completed merely because its video was watched.

## Next action

Ask for or inspect the first actual course question, preserving the source wording and course sequence. Independently reason through it before evaluating the learner's answer. Continue the timing log only with timestamp information that can be verified.

## Handoff state template

At every model handoff, update this file or provide a compact appended session entry containing:
- timestamp and timezone;
- elapsed wall-clock time if verifiable;
- focused study time if known;
- breaks actually taken;
- course topics discussed;
- exact questions reviewed;
- verified learner understanding;
- misconceptions and their corrections;
- unresolved questions;
- source screenshots/links inspected;
- next action.

Do not reset the session clock during a model handoff. Do not infer elapsed study time from wall-clock time alone.

---

## Session Log

### Timing method (agreed with learner)

Every checkpoint is committed to this file on `trunk`. **The git commit timestamp is the authoritative clock**; times written in entries are learner reports. If they disagree, the commit timestamp wins for elapsed-time math. Both Claude and ChatGPT write here — read the latest version before editing, append rather than overwrite.

**What counts as study time:** everything inside the session window, including building the "lab" (handoff specs, chatting with Claude/ChatGPT, this log). The learner deliberately did the setup inside the window, not beforehand, so the measured total reflects the real cost of a course week.

Videos were binge-watched before this session and are not counted in this session's clock.

### Session 1 — 2026-10-11 local (UTC−3) / 2026-10-12 UTC

| Event | Local (UTC−3) | UTC | Source |
|---|---|---|---|
| Session start (confirmed actual) | 2026-10-11 21:00 | 2026-10-12 00:00 | learner |
| Lab setup with Claude + ChatGPT (counts as study) | 21:00 → ~21:43 | 00:00 → ~00:43 | learner + commits |
| ChatGPT creates this file on trunk | 21:39:35 | 00:39:35 | commit 218a777 |
| Learner reports "09:38" (= 21:38) | 21:38 | 00:38 | learner |
| Start confirmed as continuous; Claude log merged here | ~21:44 | ~00:44 | this commit |

Course status at session open (from screenshot): Key Images ✅ · Discussion: Randomized Benchmarking ✅ · Qubit Robustness, Trapped-Ion, Superconducting partially complete · What Makes a Good Qubit Modality?, Qubit Modalities, Week 2 Quiz not started.

Next planned break: ~00:00 local (≈3 h after start).
Next: Section 1 — What Makes a Good Qubit Modality? (1 question).

#### Questions reviewed
_(none yet)_

#### Misconceptions / failure log
_(none yet)_

#### Breaks
_(none yet)_

### Repo note
Claude's earlier copies of this log went to `main` (commits 97ecc3e, 1043549) before `trunk` was designated the working branch. `trunk` is canonical. `main` and `master` still exist; deleting/merging them is the learner's call.


### Bitacora convention clarification
Timestamp: use this entry's Git commit metadata (UTC) as the authoritative timestamp.

Albert clarified that this is a living, append-only log (bitacora), not a static document to rewrite. Preserve all existing entries. Add new timestamped commentaries, observations, insights, decisions, corrections, and checkpoints at the bottom in chronological order. Correct historical statements by appending a dated correction, not by silently editing the earlier entry.

Albert, ChatGPT, and Claude collaborate against the same live working branch: `trunk`. Before each write, fetch the latest version from `trunk` and append to it so teammates' changes are preserved. Commit directly to `trunk`. No feature branch or pull request is needed for this text-only experiment.

The log records the real experience and cost of completing Week 2, including setup and coordination performed inside the session window. Use Git commit metadata for committed checkpoint timestamps; label user-reported clock readings with their timezone. Never invent timestamps or equate elapsed wall-clock time with focused study time.


### Checkpoint — Monday 2026-10-12, learner reports 10:12 UTC−3 (Claude)
Timestamp: this entry's Git commit metadata (UTC) is authoritative.

**Session 1 end time: NOT recorded.** The last Sunday-night checkpoint is the 22:00–22:22 UTC−3 work on Section 1 (Q1 Physical Requirements loaded, no-spoiler). Work resumed Monday morning; Claude chat message timestamps show the first Monday message at 06:59 UTC−3. The overnight gap is not study time. If Albert supplies the Sunday stop time, append it as a correction.

**Monday work so far (chat timestamps, UTC−3):**
- 06:59 · Recovered the lost forum-participation discussion (ChatGPT handoff); record delivered in chat.
- 07:02 → ~07:55 · Forum post: Discussion "Randomized Benchmarking and Gate Fidelity". Radar chart `assets/Figure_gate_fidelity.png`. Final thesis: RB vs process tomography are complementary on paper but compete for lab time and budget in practice. Citation Magesan et al. PRL 106, 180504 (2011).
- Voice session: moonshot conversation (coherent vs incoherent errors, T1/T2, crosstalk, leakage); `moonshot.md` created ~11:24 UTC.
- Q1 Physical Requirements: 1/1. Logged in `week-2-quiz-log.md`.
- 08:45 → 08:53 · Section 3 Q1 NV Centers: 1/1, first attempt, after checking the draft selection against transcript Q1M2V4a before submitting. Logged in `week-2-quiz-log.md` (commit 1533779, 11:53:19Z).
- 10:12 · Learner checkpoint. Now on Discussion: "Trapped Ions in Quantum Computation".

**Breaks:** a gap exists between 08:53 and 10:12 UTC−3; whether it was a break or offline video watching is not confirmed.

**Next:** Trapped-ion forum post, then remaining Qubit Modalities practice questions (neutral atoms / trapped ions / superconducting + other).


### Week 2 Quiz result and postmortem — recorded Wednesday 2026-10-14 ~00:10 UTC−3 (Claude, from Albert's completion record)
Timestamp: this entry's Git commit metadata (UTC) is authoritative.

**Result:** Week 2 Quiz 9.75/10 (97.5%). Week 1 was 9/10.

**Completion time (as recorded by Albert):** Tuesday 2026-10-13. Reference clock reading: a conversation screenshot showing 00:05 GMT−3. This is a conversation clock reading, not a verified quiz-submission timestamp. Keep the two separate unless the platform confirms they are the same.

**Question 7:** −0.25, partial credit on a "Select all that apply" question. Not established whether the response omitted a correct option, included an incorrect one, or both. Recorded as a partial-credit loss, not a confirmed wrong answer.

**What went well:**
- Bloch sphere question solved by voice alone, without the visual material.
- Careful reading of the qubit-modality comparison table, in particular two-qubit gate fidelity vs gate-operation time.

**Lessons:**
- Source material and exact question wording are the primary evidence.
- Distinguish an incomplete answer from one containing a wrong selection.
- Record observed scores separately from hypotheses about the grading algorithm.
- Keep strategies that worked, including audio-only Bloch sphere reasoning.
- A statement can be technically true and still not answer what the course asks; check wording and context.

**Open items:**
- Ask the course team how multi-select partial credit is computed when correct and incorrect selections are combined.
- Session 1 end time and total study time still not recorded.
- Case Study: Superconducting, 2 Study Concept Questions (Superconducting Qubits, Josephson Junction): status not reported here; last snapshot 0/2. Platform due date 2026-11-02 20:30 −03.
- The 24 h target (wrap by 20:55 UTC−3 on 2026-10-12) was not met: the quiz completion date is 2026-10-13.

**Discrepancies flagged by Claude, not silently corrected (Albert to confirm):**
1. The completion record says "19 questions". The course page shows "Week 2 Quiz (30 min) (10 Questions)" and the score is out of 10. Probably a typo for 10.
2. The record pairs "00:05 GMT−3" with "Tuesday October 13". The message delivering the record arrived Wednesday 2026-10-14 00:09 UTC−3, so the 00:05 reading may be Wednesday 00:05 (quiz finished late Tuesday) rather than Tuesday 00:05. Confirm which.


### Redaction note (Claude, Mon 2026-10-19 ~04:10 UTC−3)
Timestamp: this entry's Git commit metadata (UTC) is authoritative.

By Albert's instruction, correct options and selections for course questions were removed from this file and from `week-2-quiz-log.md`. This repository is public and answers are never published. Git history was deliberately not rewritten. This is the one sanctioned exception to the append-only rule.
