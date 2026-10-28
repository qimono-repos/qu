# JOURNAL · Week 4 · "The Finale I"
## MIT xPRO QCFx1 · Introduction to Quantum Computing
### Week 4: A Simple Quantum Algorithm in Practice (4–5 hrs) · last week of Course 1, certificate on the line

Living, append-only journal, same conventions as `week-3-experience.md`: fetch the latest `trunk` before writing, append at the bottom, correct by appending a dated correction. **Git commit metadata is the authoritative clock.** Times written in entries are learner reports, in Paramaribo time (UTC−3, no DST).

Companion file: `week-4-watch-guide.md` (video guide, graded-item list, milestones). Practice specs: `specs/week-4/`.

## Publication rules

1. **No answers.** Quiz and practice-question answers, and Albert's saved or submitted selections, are never published here. Questions and options may be stored for study.
2. **No names of other people.** Do not name anyone other than Albert Gruning in this repo or any other shared surface (Slack, Todoist, forum drafts committed here). Refer to people by role ("an instructor", "a teammate", "a graduate"). The only exception is LinkedIn direct messages, and even there any person's name is flagged to Albert and confirmed with him before use.

## Clock

| Event | Paramaribo (UTC−3) | UTC | Source |
|---|---|---|---|
| Week 4 opens (course) | Sun 2026-10-25 21:00 | Mon 2026-10-26 00:00 | `week-4-watch-guide.md` |
| Week 4 clock start (Albert) | Mon 2026-10-26 09:00 | Mon 2026-10-26 12:00 | learner, reported Tue 2026-10-27 09:55 |
| Journal opened | Tue 2026-10-27 ~10:00 | Tue 2026-10-27 ~13:00 | this commit |
| Target: every graded item submitted | Sun 2026-11-01 | | watch guide |
| **Hard deadline: course ends, forums lock** | **Mon 2026-11-02 20:30** | **Mon 2026-11-02 23:30** | course |

Note: the watch guide planned the start for Sun 21:00; the actual start was Mon 09:00 (12 h later). The plan's Tue to Sat practice block is unaffected.

## State at journal opening (Tue 2026-10-27 09:55)

All Week 4 content seen: videos and exercises (first pass). No graded items reported as submitted yet.

## Up next

1. **Answer all graded questions.** Circuit Models (2), Deutsch-Jozsa (1), Quantum Software (1), IBM QE: QASM (16), Lab Practicum IBM QE Deutsch-Jozsa (15% of the course grade, biggest open block), Week 4 Quiz (5), Post-Assessment (5% of the grade). One attempt each; Save before Submit.
2. **Forums.** Participate in the Week 4 discussions. Carry-over from Week 3: the "edX time estimation vs reality" post (data in the Week 2 and Week 3 logs) and follow-ups on earlier threads.
3. **LinkedIn.** Participate in the course's dedicated LinkedIn group and post there for teammates and graduates of earlier cohorts.

Standing after Week 3 (for reference): 74% weighted, 60% to pass. Post-Assessment and the Lab Practicum are 20 of the 26 missing points.

## Framework news

- **Slack connector:** a shared Slack workspace is now the channel where Albert, Claude and ChatGPT talk and exchange files. Claude's roles there include **time tracker** for the course. Introduction in the MIT channel: **posted** Tue 2026-10-27 ~10:00 UTC−3 (#mit).
- **Todoist connector:** the "Up next" list above now lives in Todoist under the MIT project: **done** Tue 2026-10-27 ~10:00 UTC−3 (3 tasks, 10 subtasks).

## Log

<!-- Append entries below: ### <what> (<who>, <day date ~time UTC−3>) -->

### Slack intro posted, Todoist tasks created (Claude, Tue 2026-10-27 ~10:00 UTC−3)

- **Slack:** Claude's introduction posted in #mit (role: time tracker for the course, journal keeper, drafting help for forum and LinkedIn posts, study and sparring partner; states the hard deadline Mon 2026-11-02 20:30 UTC−3).
- **Todoist, project MIT:**
  1. "Week 4: answer all graded questions" · due Sun 2026-11-01 · P1 · 7 subtasks: Circuit Models (2), The Deutsch-Jozsa Quantum Algorithm (1), Quantum Software (1), IBM QE: QASM (16), Lab Practicum IBM QE Deutsch-Jozsa (N=1, N=3, 15%), Week 4 Quiz (5), Post-Assessment (5%).
  2. "Week 4: forum participation" · due Mon 2026-11-02 18:00 (forums lock 20:30) · P2 · 3 subtasks: Week 4 discussion threads, "edX time estimation vs reality" post (data in `week-2-experience.md` and `week-3-experience.md`), follow-ups on earlier threads.
  3. "Week 4: LinkedIn — post in the course's dedicated LinkedIn group for teammates and graduates" · due Sun 2026-11-01 · P3.
- Note: Todoist hard "deadline" fields are a premium feature on this account, so only due dates are set; the 20:30 hard deadline is written in the task descriptions instead.
- Framework news above updated from "pending" to done.

### Todoist mirror of the edX outline (Claude, Tue 2026-10-27 ~10:06 UTC−3)

- New task `WEEK-4-MIT-TRACK` in the MIT project: 7 sections and 18 items, titles copied exactly from the edX Week 4 outline. Items already done on edX at that time were ticked off (11), including the whole "IBM QE: Deutsch-Jozsa Algorithm (2 hr)" section and "Key Images".
- Open question for Albert: the edX outline shows the Deutsch-Jozsa lab section as complete. If that means the Lab Practicum (15%) is submitted, the matching subtask in "Week 4: answer all graded questions" should be closed too.

### First practice solved: Circuit Models · Classical Circuit Model · Q1 "Number of Gates" (Albert + ChatGPT + Claude, Tue 2026-10-27 ~12:23 UTC−3)

- **Result: 1.0 / 1.0 point, on attempt 1 of 2.** Graded result and course explanation posted by Albert in the Slack thread at 12:31.
- How it went: ChatGPT framed the problem and a candidate in a `#mit` thread (11:57). Albert posted the options and his saved, unsubmitted selection (11:59), asking for an unbiased check. Claude verified independently (12:02) and posted the exhaustive Python check and truth table (12:08). Albert submitted.
- **Method lesson (no answer content):** for "minimum number of gates *following the procedure*" questions, count the **unique** gate operations across all output equations; a sub-expression shared by two outputs is built once and **reused**. The course explanation used exactly this reuse argument.
- edX outline after submission: "Classical Circuit Model" shows the green done icon; "Quantum Circuit Model" (Circuit Models, 2nd question) still open.

### Slack protocol adopted (Claude, Tue 2026-10-27 ~12:35 UTC−3)

- `#mit` is now the team's **service bus**: one thread per exercise, independent verification before comparing with Albert's pick, **keywords** marked in questions and explanations, a "done" message with links after every assigned task.
- Rule change: **Slack is the answer-sharing space.** Answers may be posted there; this repo still never stores answers (Publication rule 1 unchanged).
- Full protocol: [`slack-protocol.md`](slack-protocol.md).

### Slack protocol change: minimum memory before posting (Claude, Tue 2026-10-27 ~12:46 UTC−3)

- Requested by Albert. New §3 in [`slack-protocol.md`](slack-protocol.md): before posting, every participant reads the latest message where they're about to post (the thread's last reply, or the channel's last message plus its thread), opens any attachments, and accounts for what changed. Agents without session memory also re-read the thread parent.
- Later sections renumbered (§4 to §9).

### Classical-circuits mini-projects on trunk (ChatGPT, Tue 2026-10-27 ~12:50 UTC−3)

- Reported by ChatGPT in `#mit`: new `src/circuits/classic/` with a Python `uv` project (pytest), a Jupyter notebook and a Clojure CLI project (`deps.edn`), each implementing and exhaustively checking the 2-bit × 2-bit Boolean multiplier from the Circuit Models lesson. Local runs of `uv`, Jupyter and the Clojure CLI are still pending.
- Open question for Albert: these projects implement the gate construction that the Classical Circuit Model practice asks about. The practice is already graded, but Publication rule 1 says answers never go in this repo. Confirm whether lesson implementations like this are allowed after grading, so the rule can say so explicitly.

### Slack protocol v2: message types, reaction states, offsets (Claude, Tue 2026-10-27 ~13:05 UTC−3)

- Requested by Albert after a discussion of how the protocol compares with Kafka and a service bus. Changes in [`slack-protocol.md`](slack-protocol.md):
  - **§3 Offsets:** "read the last message" became "consume from your offset": read everything after your own last message in that thread. With no prior message there, read the parent and the whole thread.
  - **§4 Message types:** every message starts with an inline-code label: `REQUEST`, `ACK`, `NACK`, `RESULT`, `DONE`, `CORRECTION` or `INFO`. The first `ACK` from a tagged owner claims the item, and every `REQUEST` must end in `DONE`, `NACK` or a cancelling `CORRECTION`.
  - **§5 Reaction states on the REQUEST:** 👀 ACKed, ✅ done, ❌ NACKed, ♻️ superseded.
  - A table mapping bus concepts to Slack; §12 roadmap toward Bluesky, Microsoft Teams groups and a dedicated Kafka VM. Sections renumbered (§1 to §12).
- Announced in `#mit` as a `REQUEST` to Albert and ChatGPT, with a how-to and a worked example; each participant replies `ACK` in that thread when ready.

### Second practice solved: Circuit Models · Quantum Circuit Model · Q1 "Number of Summands and Normalization" (Albert + ChatGPT + Claude, Tue 2026-10-27 ~14:15 UTC−3)

- **Result: 1.0 / 1.0 point, on attempt 1 of 2.** Screenshot posted by Albert in the `#mit` thread at 14:15. With this, both Circuit Models questions are done.
- How it went: the thread was opened at 13:20 with the verbatim course text. Albert posted the practice image as a `REQUEST` (13:27), and all three participants `ACK`ed that they could see it before any analysis (first use of protocol v2). Albert and ChatGPT reached a verdict on a live audio call and asked Claude for a third opinion (14:03). Claude confirmed it independently with a derivation and a numpy check (14:08), flagging that the option saved at the time was a trap and should be switched before submitting.
- **Method lesson (no answer content):** read **"normalizing coefficient"** as the *amplitude* in front of each basis state, not the measurement *probability* (its square). Wrong options tend to be real quantities in the wrong place, so name what each one actually is.

### New utility: `superposition-stats` (Claude, Tue 2026-10-27 ~14:28 UTC−3)

- Requested by Albert: the numpy check from the practice became a reusable terminal utility in two languages, under `src/circuits/quantum/` (next to ChatGPT's `src/circuits/classic/`):
  - `python/`: `uv` project, `uv run superposition-stats 4`, pytest suite.
  - `babashka/`: `bb superposition-stats 4`, `bb test`, no dependencies.
- It reports summands, amplitude and probability per outcome for H^⊗n |0…0⟩. Unit tests assert the 3- and 4-qubit cases and reject invalid n.
- Verified: Babashka tests pass (3 tests, 9 assertions). The Python CLI and all 6 Python test cases pass, run through a stdlib stand-in for pytest because PyPI wasn't reachable from Claude's sandbox. A real `uv run --extra test pytest` locally is still pending.
- Commit: `b09ca7d`.

### Slack protocol v2.1 (Claude, Tue 2026-10-27 ~14:30 UTC−3)

- Requested by Albert in the Quantum Circuit Model thread. Two additions to §6 of [`slack-protocol.md`](slack-protocol.md):
  - Before any work, confirm whether the question is **select only one option** or **select all that apply**.
  - Every `RESULT` gives a verdict for **every option**: why each selected option is TRUE, and why each unselected option is FALSE.

### First job for local-opencode: real pytest run + packaging fix (local-opencode + Claude, Tue 2026-10-27 ~14:38 to 14:59 UTC−3)

- **New participant on the bus:** local-opencode, an AI agent running on Albert's own machine, reached through Albert. Claude sent it a `REQUEST` in `#mit` (14:38) because PyPI wasn't reachable from Claude's sandbox.
- **`RESULT` `DONE` (14:58):** both CLI outputs exact, **pytest 6 passed** (pytest 9.1.1, Python 3.12.12, uv 0.10.12), `bb test` 3 tests / 9 assertions / 0 failures (babashka 1.13.219).
- **Fix `dfb29b5`** (`fix(quantum):`): hatchling couldn't auto-discover the package, because the project name `qimono-quantum-circuits` doesn't match the folder `quantum_circuits/`. It now has `[tool.hatch.build.targets.wheel] packages = ["quantum_circuits"]` in `pyproject.toml`. Tests unchanged. Claude's stand-in runner imported from the source folder and never built a wheel, so it couldn't catch this. **Lesson: verify with the real toolchain before calling it done.**
- Machine note, not a repo change: on Albert's Guix system, `uv run` needs `LD_LIBRARY_PATH` pointing at the Guix zlib (`…-zlib-1.3.1/lib`).
- Follow-up flagged in `#mit` (`INFO`, unassigned): `src/circuits/classic/python/pyproject.toml` has the same name/folder mismatch and likely needs the same fix.

### Deutsch–Jozsa practice opened; first `CORRECTION` on the bus; protocol v2.2 (Claude, Tue 2026-10-27 ~15:12 to 15:20 UTC−3)

- New thread for **The Deutsch-Jozsa Quantum Algorithm** (opened by ChatGPT at 14:48). Practice: *Q1 Balanced and Constant Functions*, two dropdowns, one choice each, **0 of 3 attempts used**, answers saved but not submitted. Only Albert and Claude had the screenshot, so Claude posted a text narration for the other agents (15:11), without revealing the saved selections.
- Albert corrected the rule: keywords are **allowed and encouraged**. Claude posted the bus's first `CORRECTION` (15:16), linking the narration and marking it ♻️, with an extended keyword set: definitions, wording cues, the four one-bit functions, the bridge to the algorithm (oracle, query complexity, parity, phase kickback, global vs relative phase), and traps.
- [`slack-protocol.md`](slack-protocol.md) v2.2: §7 now says keywords are encouraged at every stage and gives a checklist (definitions, wording cues, method hints, spoiler-level context, traps; never the answer). In §4 and §5, a `CORRECTION` can amend as well as supersede.

### Third practice solved: The Deutsch-Jozsa Quantum Algorithm · Q1 "Balanced and Constant Functions" (whole team, Tue 2026-10-27 ~15:45 UTC−3)

- **Result: 1.0 / 1.0 point, on attempt 1 of 3.** Four independent verdicts agreed (local-opencode, ChatGPT, Claude, and Albert's own saved selection) before submission. The edX outline now shows *Circuit Models* and *The Deutsch-Jozsa Quantum Algorithm* complete.
- **How the course author reasons (method lesson, no answer content):** the official explanation defines *constant* as "output **independent of the input**" and *balanced* distributionally: "**uniform input ⇒ uniform output**". The wording "binary, uniformly distributed variable" in the question pointed to that definition; it was not a distractor (Claude's earlier keyword note called it a possible trap, now corrected in Slack). Caveat: "input-dependent ⇒ balanced" holds for one bit (any non-constant 1-bit function is a bijection) but not for n ≥ 2 bits, which is why Deutsch–Jozsa needs the *promise*.
- **Awareness raised:** nobody asked whether picking an option in one dropdown removes it from the next (it doesn't; each dropdown is independent). Added to the protocol, with a call for more follow-up questions.
- Todoist `WEEK-4-MIT-TRACK`: "The Deutsch-Jozsa Algorithm" and its section "The Deutsch-Jozsa Quantum Algorithm (10 min) (1 Question)" marked done. *Circuit Models* was already closed.
- [`slack-protocol.md`](slack-protocol.md) v2.3: §6 now also confirms whether options can repeat across parts, and explicitly encourages follow-up questions.


### Slack protocol v2.4: operational thread closure (ChatGPT, Tue 2026-10-27 ~15:58 UTC−3)

- Added §13 to [`slack-protocol.md`](slack-protocol.md): a Slack exercise thread is **protocol-closed, not technically immutable**. The available integration has no dedicated ordinary-thread close/lock action.
- Standard closure sequence: read to the head (including replies, attachments, corrections and reactions); verify the graded outcome; verify both the relevant Todoist child and parent/container; post a final `DONE` with result and links; add ✅ to the parent/request; leave the thread available for audit and corrections. Never claim a thread is technically closed unless a tool confirms it.
- Clarified routing: protocol changes are announced as a top-level `INFO` or `REQUEST` in `#mit`; discussion goes in that announcement's thread.
- Commit: `41a7d7634a74067f0d5b175a464352537dde142b`.

### Fourth practice solved: Quantum Software · Programming Tools · Q1 "Quantum Circuit Design" (whole team, Tue 2026-10-27 ~17:04 UTC−3)

- **Result: 1.0 / 1.0 point, on attempt 1 of 2.** Single-choice (radio). Four independent verdicts agreed before submitting (ChatGPT, local-opencode, Claude, Albert's saved choice). Todoist: "Programming Tools" and its section "Quantum Software (15 min) (1 Question)" marked done by ChatGPT.
- **Resource-first paid off:** Albert supplied the full lesson video transcript before submission. The deciding line (02:18, "noise and error is a major concern…") and the course's own definition of qubit *performance* (coherence time, noise sensitivity, 02:50–03:03) turned a general-knowledge answer into a course-aligned one, and showed the "temporal" distractor was a fragment of the right answer.
- **Method lesson (no answer content):** the post-submit explanation was one sentence, a near-paraphrase of the transcript line. For concept questions, the **transcript is the best predictor** of the course's answer; post-submit explanations are short confirmations. The video's "**as mentioned earlier**" also shows concepts can come from *earlier* lessons, so a resource request should include earlier transcripts when the wording points back.
- Relay note: local-opencode's verdict table lost its cells when copied from the terminal into Slack. Claude's note blaming the formatting was corrected in the thread. When a local-opencode answer has a table, Albert attaches a terminal screenshot as well.
- Open: local-opencode reported the protocol commit `a8f3d92` ("Resource-first" step in §6) as pushed, but at ~17:15 it was not on `trunk` (head `65c4db1`) or any other remote branch. Flagged in the thread; the commit still needs to be pushed.

### Fifth practice solved: IBM QE: QASM · Syntax of QASM · Q1 "Syntax Error I" (whole team, Tue 2026-10-27 ~18:33 UTC−3)

- **Result: 1.0 / 1.0 point** (single choice, 4 attempts available). The team flipped Albert's original saved pick after gathering evidence: the OpenQASM 2.0 spec (arXiv:1707.03429, §2: "Whitespace is ignored"), Albert's VS Code run of the exact snippet (OpenQASM + QDK extensions: 0 errors, simulated, circuit drawn) and the lesson's own example. No IBM account was needed.
- **How the course author reasons (method lesson, no answer content):** the post-submit explanation is explicitly **environment-specific**: it is about what "the current instance of IBMQ" accepts, and says other environments might differ. The course's reference parser is IBM's, so for syntax questions, test in an IBM/Qiskit-compatible OpenQASM 2.0 parser and read the answer as "what IBMQ accepts", not as a universal rule.
- **Evidence hygiene:** local-opencode's first parser run and kata used `include "qelib1.inc";` (with a space), so they didn't test the line in doubt. Claude caught it by checking the committed file byte by byte. Albert fixed the kata to the exact exam spelling (`19a66a4`), and local-opencode re-ran it on the exact bytes: clean. **Lesson: test inputs must match the question byte-for-byte.**
- Local line numbers are +1 versus edX, because the local file adds the `OPENQASM 2.0;` header. Kata: `first-code/practice/katas/syntax_error1.qasm`.
- Still open: (1) whether `qasm_check.py` accepts a header-less file or adds the header itself (asked, not answered yet); (2) Albert's decision on course katas and answers in the repo after grading (Publication rule 1); (3) Todoist "Syntax of QASM" stays open until all of that page's questions are done (the "I" suggests a series).

### Overnight session summary: Syntax of QASM, Measurements, Single-Qubit Gates, IBMQx4; Grok joins; protocol v2.5 (Claude, Wed 2026-10-28 ~06:45 UTC−3)

- **Progress, all graded 1.0/1.0** (score and attempts only, per Publication rule 1): Syntax of QASM Q2–Q5 (5/5 page complete); Measurements Measuring I–VIII (8/8, every one on the first attempt); Single-Qubit Gates I–II. IBMQx4 I proposed by all agents, submission pending at the time of writing.
- **Team:** Grok joined the bus on Tue ~22:30 as a native Slack app (can't read images, so screenshots are narrated and diagrams drawn as "ugly art"). local-opencode ran out of quota for the night. A Linear integration was added to `#mit`.
- **CI:** the QASM katas workflow became "Quantum Katas CI": fails on any unexpected parse error, emits file/line annotations, writes a step summary and prints circuit diagrams. PR #5 adds a measurement-mapping script; Claude ran it locally and it matched the team's forecast, with the caveat that it encodes our convention rather than testing it.
- **Course feedback found:** a duplicated option in a Measurements diagram question; a likely erratum in the Single-Qubit Gates table (T† entry); a forum post about "transposed" labels that is actually the ket-vs-label notation (draft reply prepared for Albert). Forum draft with hints (no answers) for the Measurements practice prepared.
- **Protocol v2.5** ([`slack-protocol.md`](slack-protocol.md)), requested by Albert: Grok added to §1; §6 steps renumbered (there were two "3."); §8 adds image narration, full "ugly art" for every option, and the Slack-has-no-LaTeX note; new §14 distractor taxonomy; new §15 conventions and lessons learned (ket |q0 q1 …⟩ vs label c[n−1]…c[0], byte-exact inputs, reported ≠ source line, directed coupling maps, CI-as-witness caveat).
