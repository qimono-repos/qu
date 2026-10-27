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
