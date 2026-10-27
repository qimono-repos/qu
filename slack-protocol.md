# Slack protocol · Qimono `#mit`

How Albert, Claude, ChatGPT and local-opencode use the Qimono Slack workspace for the MIT xPRO course.
Living document: change it by committing to `trunk` and logging the change in the current week's journal.

Started Tue 2026-10-27, Week 4 of QCFx1. Times are Paramaribo time (UTC−3).
v2, Tue 2026-10-27 ~13:05: message types (§4), reaction states (§5), offset-based reading (§3).
v2.1, Tue 2026-10-27 ~14:30: question type confirmed first, and a TRUE/FALSE verdict for every option (§6).

## 1. What the channel is

`#mit` is our **service bus**. Every participant publishes requests, results and status to it, and every participant reads from it. Nobody depends on private side-channels to know what the others did.

| Participant | Role on the bus |
|---|---|
| Albert Gruning | Learner and owner. Submits on edX, posts problems and course feedback, assigns work, has the final say. |
| Claude | Time tracker, journal keeper (`qu` repo), independent verifier, study and sparring partner. |
| ChatGPT | Problem framing, first-pass solutions, code projects, Todoist bookkeeping when asked, independent verifier. |
| local-opencode | Agent on Albert's own machine, reached through Albert (address it as `@local-opencode`, plain text). Runs the real toolchain (`uv`, pytest, `bb`, Qiskit) and may commit fixes to `trunk`. |

A message tagged to one agent is that agent's work item. The other agent may comment, but doesn't take the item over.

Bus mapping, for orientation:

| Service bus / Kafka | Slack `#mit` |
|---|---|
| Topic / queue | The channel (announcements) or one thread (one exercise or one work item) |
| Message type / header | The type label on the first line (§4) |
| Addressing / routing | `@mention` of the owner |
| Peek-lock, claim | `ACK` (👀 reaction) by the owner |
| Complete | `DONE` (✅ reaction) |
| Dead-letter / reject | `NACK` (❌ reaction) |
| Consumer offset | Your own last message in that thread or channel (§3) |

## 2. One thread per exercise

- Every practice question and every quiz question gets **its own thread**. The parent message is the problem: statement, options (a screenshot is fine) and course context.
- Everything about that exercise stays in the thread: verification, code, tables, the result, the course explanation and lessons learned.
- New exercise, new thread. Don't continue an exercise in the main channel.
- Announcements and work that isn't tied to one exercise (protocol changes, repo drops) go in the channel as a parent message, and the follow-ups go in its thread.

## 3. Minimum memory before posting: consume from your offset

**Before posting anything, read everything from your offset to the head of the place you're about to post in.** This is a hard requirement for every participant, human or agent.

- **Your offset** is your own last message in that thread (or in the channel, for top-level posts). Read every message after it, not just the newest one.
- **No previous message of yours there** (new thread, or an agent without session memory): read the thread parent and the whole thread. In the channel, read at least the last 3 top-level messages and open any of their threads that have new replies.
- **Files count:** open attachments (screenshots, code) in the messages you consume.
- **Check the state reactions** (§5) on the messages you consume: a ✅ means that work is already done, and a 👀 means someone owns it.
- If what you read changes the picture (a result posted, a task already done, a correction, a new request), your post must take it into account, or not be sent at all.

Why: several participants post on the same bus, agents can lag behind it, and Slack doesn't store per-reader offsets the way Kafka does. Each reader works out their offset from their own last post.

## 4. Message types

Every message on the bus starts with **one type label in inline code** on the first line, followed by who it's for and what it refers to:

```
`TYPE` → @owner · re: <link to the message it answers> · short subject
```

| Type | Meaning | Must contain |
|---|---|---|
| `REQUEST` | Asks for work. | An `@owner` for each part, the definition of done, a due time if there is one. |
| `ACK` | "I've read this and I own it" (peek-lock). | Optional: ETA, scope, questions. A 👀 reaction alone is a valid ACK. |
| `NACK` | "I can't or won't do this." | The reason, and what would unblock it. Add ❌ to the REQUEST. |
| `RESULT` | Work product: answer, verification, code, table. | Evidence, not just a verdict. |
| `DONE` | Closes a REQUEST. | Links to what was produced (commit, file, Todoist item). Add ✅ to the REQUEST. |
| `CORRECTION` | Supersedes an earlier message. | A link to the corrected message and what changed. Add ♻️ to the corrected message. |
| `INFO` | For the record, no action needed. | Status, announcements, FYIs. |

Rules:
- **One primary type per message.** `RESULT` + `DONE` together is fine when the result closes the request: write `` `RESULT` `DONE` ``.
- **Ownership:** the first `ACK` from a tagged owner claims the item. Anyone else who wants to help comments in the thread, without claiming it.
- **Every REQUEST ends in exactly one of `DONE`, `NACK`, or a `CORRECTION` that cancels it.** Nothing is left hanging.
- Labels are plain text, so Slack search finds them: search `` `REQUEST` in:#mit `` to see open work.

## 5. Reaction states (on the REQUEST message)

Reactions are the status field of a REQUEST, readable at a glance without opening the thread:

| Reaction | Slack code | State |
|---|---|---|
| 👀 | `:eyes:` | ACKed: the owner has read it and claimed it |
| ✅ | `:white_check_mark:` | DONE |
| ❌ | `:x:` | NACKed |
| ♻️ | `:recycle:` | Superseded by a CORRECTION (on the corrected message) |

The reaction never replaces the `DONE` or `NACK` message, which carries the links and reasons. It just mirrors the state.

## 6. Solving loop (exercises)

1. **Frame.** `REQUEST` parent message: the question, options and the relevant lesson material.
   **Question type first:** before any work starts, the framer states, or asks for confirmation of, whether the question is **select only one option** (radio buttons) or **select all that apply** (checkboxes). Every participant confirms it in their `ACK`.
2. **Tentative selection.** Albert may say what he picked (saved, not submitted). Agents must **not let it bias them**. They derive from scratch first and compare after.
3. **Independent verification.** Each agent posts a `RESULT` answering the questions asked one by one: assert or refute, and give a counterexample when refuting. Evidence beats agreement: exhaustive checks, truth tables, derivations.
   **Every option gets a verdict:** for each option judged correct, say **why it is TRUE**; for each option judged incorrect, say **why it is FALSE** (e.g. "right count, but that's the probability, not the coefficient"). Distractors are usually a real quantity in the wrong place, so naming what each one actually is guards against traps.
4. **Submit.** Only Albert submits on edX. Edits to the Save state and attempts are his.
5. **Result.** Albert posts the graded result and the course's official explanation (`INFO`) in the thread.
6. **Alignment check.** Agents confirm whether the official explanation matches the reasoning used, name any difference in method, and extract a **reusable rule** for similar questions.
7. **Close.** Claude logs the outcome in the week's journal (score and attempt only, see §9), the Todoist item is marked done by whoever was tagged, and the parent gets ✅.

## 7. Keywords

Mark the **keywords** of a question or explanation whenever they help: the words that decide what the question is actually asking. Examples: *"following the procedure in the video"*, *"minimum number of gates"*, *"unique"*, *"reuse"*. Bold them in Slack, and say why they matter (e.g. "minimum" is relative to the course's procedure, not an absolute circuit-complexity bound).

## 8. Message format

- Slack renders Markdown: **bold**, `code`, fenced code blocks with a language tag, and pipe tables. Use tables for truth tables and comparisons, and code blocks for runnable snippets.
- Snippets must run as posted (imports included, stdlib preferred) and print a clear pass/fail line.
- Agents sign their messages ("Claude here", "Iam Chat GPT", or the app's "Sent using" footer) so the bus stays readable. All agents currently post through Albert's account, so the signature is the only way to tell senders apart.

## 9. What may be posted where

| Content | Slack `#mit` | `qu` repo | Todoist |
|---|---|---|---|
| Practice / quiz answers and Albert's selections | Yes, Slack is the answer-sharing space | **No** | No |
| Verification code, truth tables, derivations | Yes | Only if they don't reveal a graded answer | No |
| Scores, attempts used, timestamps | Yes | Yes | In task comments if useful |
| Names of anyone other than Albert Gruning | **No**: use roles ("an instructor", "a teammate") and ask Albert first if a name seems needed | **No** | **No** |

## 10. Clock

Slack message timestamps and Git commit timestamps are both machine clocks. The journal's times are learner reports. When they disagree, Git commit metadata wins for the journal, and Slack timestamps are supporting evidence.

## 11. Where things live

- Weekly journal: `JOURNAL-week-<n>.md` (current: [`JOURNAL-week-4.md`](JOURNAL-week-4.md))
- Earlier weeks: `week-2-experience.md`, `week-3-experience.md`
- Tasks: Todoist project **MIT** (`WEEK-4-MIT-TRACK` mirrors the edX outline for Week 4)

## 12. Roadmap (not active yet)

The same message model is meant to carry over to other platforms: Bluesky, Microsoft Teams groups, and a dedicated Kafka instance on a VM. The types in §4 are designed so they can become real message headers or a schema later. Slack is the first transport.
