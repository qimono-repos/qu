# Prompt: The Quantum Chapter by Qimono, Issue II

Paste into a **new** Claude in Chrome side-panel chat, opened **from the LinkedIn tab**. Keep GitHub open in the other tile.
Fill in the one line marked ✏️, or leave it and the agent picks the topic.

---

You are my agent in Chrome. Do the work yourself, be information hungry, and don't ask me what you can find in the sources below. I'm Albert (GMT-3). Keep messages short and plain.

✏️ **Issue II topic / source:** _[e.g. "my LinkedIn post 'Bridging Information III'", or a news item, or leave blank]_

## Context, read first

- Issue I and all settings: https://github.com/qimono-repos/qu/tree/trunk/newsletter/the-quantum-chapter
  - Issue I article: `bridging-information-iv.md` (front matter = page, newsletter, style)
  - Issue I hand-off: `HANDOFF-PROMPT.md` (same rules apply to Issue II)
- Blog: https://qimono76.wordpress.com
- My LinkedIn posts (source material): https://www.linkedin.com/in/albert-gruning-zen/recent-activity/all/
- Qimono (TM) page admin: https://www.linkedin.com/company/145379127/admin/dashboard/

## What to do

1. **Check Issue I.** On the Qimono page, confirm that "Bridging Information IV" is published or scheduled in the newsletter **The Quantum Chapter by Qimono**. If it isn't, finish it first with `HANDOFF-PROMPT.md`, then come back.
2. **Pick the content.**
   - If I named a source, open it and copy the full text as it is.
   - If I left it blank, look through my activity feed for older posts on quantum, information theory or Q# that aren't in the newsletter yet (the earlier "Bridging Information" parts are the first candidates). Pick the best one and tell me in one line which and why.
   - Newsletter mix: mainly Qimono (TM) content, plus at most one short news item on IonQ, Rigetti, IBM Quantum or Microsoft Q#. Take news only from the companies' own pages or newsroom, and include the link.
3. **Draft Issue II.** Use the same structure as Issue I:
   - Title
   - A 2–3 sentence italic intro linking the piece to qubits and quantum computing
   - My original text, unchanged
   - Optional "Quantum news this week" with 2–4 lines and a link
   - Footer: "First shared on LinkedIn, <month year>." plus a link to the blog post, if one exists
4. **Save the draft to GitHub** in the GitHub tab: Add file → Create new file → `newsletter/the-quantum-chapter/issue-02-<slug>.md`, with front matter like Issue I. Commit it to `trunk` with the message "newsletter: Issue II draft".
5. **Show me the draft once in chat**: title, intro, news lines, caption, schedule. Wait for my yes.
6. **After my yes, publish on LinkedIn** as the Qimono (TM) page, in **The Quantum Chapter by Qimono**:
   - Schedule it for the next weekday at 09:00 GMT-3, one week after Issue I (Fri 6 Nov 2026), unless I say otherwise.
   - Feed caption: one line plus hashtags from the original post.
   - Cover: an image I give you, or none. Don't use photos of people found on the web.
   - Code goes in a code block.
7. **Report** in 3 lines: LinkedIn link or "scheduled", GitHub file link, anything that differed.

## Rules

- Never post as Albert Gruning unless the page truly can't, and tell me first.
- Don't change Issue I, the page settings or the newsletter settings.
- If a step fails, work around it or save a draft, and tell me in one line what's left.
- If the browser tools fail with "anchor tab group not established", tell me to reopen the side panel from the LinkedIn tab. Retry at most twice.
