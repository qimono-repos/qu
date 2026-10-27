# Slack protocol · Qimono `#mit`

How Albert, Claude and ChatGPT use the Qimono Slack workspace for the MIT xPRO course.
Living document: change it by committing to `trunk` and logging the change in the current week's journal.

Started Tue 2026-10-27, Week 4 of QCFx1. Times are Paramaribo time (UTC−3).

## 1. What the channel is

`#mit` is our **service bus**. Every participant publishes requests, results and status to it, and every participant reads from it. Nobody depends on private side-channels to know what the others did.

| Participant | Role on the bus |
|---|---|
| Albert Gruning | Learner and owner. Submits on edX, posts problems and course feedback, assigns work, has the final say. |
| Claude | Time tracker, journal keeper (`qu` repo), independent verifier, study and sparring partner. |
| ChatGPT | Problem framing, first-pass solutions, Todoist bookkeeping when asked, independent verifier. |

A message tagged to one agent is that agent's work item. The other agent may comment, but doesn't take the item over.

## 2. One thread per exercise

- Every practice question and every quiz question gets **its own thread**. The parent message is the problem: statement, options (a screenshot is fine) and course context.
- Everything about that exercise stays in the thread: verification, code, tables, the result, the course explanation and lessons learned.
- New exercise, new thread. Don't continue an exercise in the main channel.

## 3. Minimum memory before posting

**Before posting anything, read the latest message where you're about to post.** This is a hard requirement for every participant, human or agent.

- **Replying in a thread:** read the thread's last message, or every reply since your own last message in that thread if there's more than one.
- **Posting in the channel:** read the channel's last message, and open its thread if it has replies.
- **Files count:** if that message has attachments (screenshots, code), open them before replying.
- If the latest message changes the picture (a result posted, a task already done, a correction, a new request), your post must take it into account, or not be sent at all.
- Agents with no memory of earlier sessions also re-read the thread parent, so they know what the exercise is.

Why: three participants post on the same bus, and agents can lag behind it. Reading the last message first prevents duplicate work, contradicting a result that's already known, or answering a question that has moved on.

## 4. Solving loop

1. **Frame.** The parent message gives the question, options and the relevant lesson material.
2. **Tentative selection.** Albert may say what he picked (saved, not submitted). Agents must **not let it bias them**. They derive from scratch first and compare after.
3. **Independent verification.** Each agent answers the questions asked one by one: assert or refute, and give a counterexample when refuting. Evidence beats agreement: exhaustive checks, truth tables, derivations.
4. **Submit.** Only Albert submits on edX. Edits to the Save state and attempts are his.
5. **Result.** Albert posts the graded result and the course's official explanation in the thread.
6. **Alignment check.** Agents confirm whether the official explanation matches the reasoning used, name any difference in method, and extract a **reusable rule** for similar questions.
7. **Close.** Claude logs the outcome in the week's journal (score and attempt only, see §7), and the Todoist item is marked done by whoever was tagged.

## 5. Keywords

Mark the **keywords** of a question or explanation whenever they help: the words that decide what the question is actually asking. Examples: *"following the procedure in the video"*, *"minimum number of gates"*, *"unique"*, *"reuse"*. Bold them in Slack, and say why they matter (e.g. "minimum" is relative to the course's procedure, not an absolute circuit-complexity bound).

## 6. Message format

- Slack renders Markdown: **bold**, `code`, fenced code blocks with a language tag, and pipe tables. Use tables for truth tables and comparisons, and code blocks for runnable snippets.
- Snippets must run as posted (imports included, stdlib preferred) and print a clear pass/fail line.
- Agents sign their messages ("Claude here", "Iam Chat GPT", or the app's "Sent using" footer) so the bus stays readable.
- **Done messages:** when an agent finishes a task assigned on the bus, it posts a short "done" message in the same thread with links to whatever it produced (commit, file, Todoist item).

## 7. What may be posted where

| Content | Slack `#mit` | `qu` repo | Todoist |
|---|---|---|---|
| Practice / quiz answers and Albert's selections | Yes, Slack is the answer-sharing space | **No** | No |
| Verification code, truth tables, derivations | Yes | Only if they don't reveal a graded answer | No |
| Scores, attempts used, timestamps | Yes | Yes | In task comments if useful |
| Names of anyone other than Albert Gruning | **No**: use roles ("an instructor", "a teammate") and ask Albert first if a name seems needed | **No** | **No** |

## 8. Clock

Slack message timestamps and Git commit timestamps are both machine clocks. The journal's times are learner reports. When they disagree, Git commit metadata wins for the journal, and Slack timestamps are supporting evidence.

## 9. Where things live

- Weekly journal: `JOURNAL-week-<n>.md` (current: [`JOURNAL-week-4.md`](JOURNAL-week-4.md))
- Earlier weeks: `week-2-experience.md`, `week-3-experience.md`
- Tasks: Todoist project **MIT** (`WEEK-4-MIT-TRACK` mirrors the edX outline for Week 4)
