# Forum post: What's the role of a university, versus a newspaper?

- Course: MIT xPRO QCFx1
- Type: new standalone thread (meta discussion, follow-up to the superconducting module thread)
- Drafted: 2026-10-14, Albert with Claude
- Status: draft, ready to post
- Origin: Albert's question, "are we asking MIT to do the role of the newspapers?"
- Revision: proposal paragraph rewritten after reading the Module 2 transcripts (V11a to V13b)
- Revision 2 (2026-10-14): source attribution corrected. The V10 intro is Prof. William Oliver and is current for 2026; only the Lincoln Lab videos (V11-V13) are the 2018 recordings. The public post must target only the clearly-dated 2018 figures, never the intro.
- Revision 3 (2026-10-14): added four-tier remediation ladder and edX platform mechanics. Tier 3 (Lincoln Lab first-party data) is the primary ask.
- Revision 4 (2026-10-14): Lincoln Lab status verified - MIT-managed FFRDC (see Notes for verification).

---

**What's the role of a university, versus a newspaper?**

A lot of us in the superconducting thread (myself included) have been pointing out that the module's numbers are old, and we mean well. But I want to question the framing of our own complaint, because I think we're quietly asking MIT to do a job that was never its job.

When we say "the content is outdated," what we often mean is "it doesn't match this week's headlines." But that's the newspaper's role, not the university's. A newspaper's value is freshness. A university's value is the opposite: teaching the things that stay true long enough to be worth learning. The DiVincenzo criteria in this module are from around 2000, and in 2026 they're still the frame everyone uses to reason about qubits. The interconnect problem, phase kickback, why coherence matters, none of that expires. A course optimized for freshness would actually be worse, because it would chase noise instead of teaching the signal. If MIT rewrote the material every time a new chip shipped, we'd learn press releases, not physics.

So I don't think the module is "outdated" in the way it first looks. The framework is doing exactly what a university should do.

But here's the one place I'd still push, and I think it's a real issue, not just a cosmetic one. There's a difference between a fact being old and a fact being wrong in a way that misleads. The good news is the course already knows how to handle this: V13a says "As of 2018" before its coherence numbers, and V12b does the same for resonator quality factors. The problem is that it isn't consistent. The opening line of V13a, "up to around a few tens of qubits", has no date, and it's the sentence that frames the whole scaling discussion. The same goes for the gate fidelities in V11b and the "100 qubits or more" plan in V13b. So my proposal is narrow: apply the "as of 2018" stamp the course already uses to those few undated figures. That's a footnote, not a subscription. I'm happy to help put the references together if the staff wants a hand.

Curious what others think: where's the line for you between content that's genuinely outdated and content that just isn't today's news?

---

## Source attribution (read before editing this post)

Two different speakers, two different dates. Do NOT conflate them.

- **V10, Superconducting Qubits: Introduction** - Prof. William Oliver. Current for 2026 (file is REV_2026_v2). His figures (e.g. processors "pushing 1,000 qubits") are his present-day framing, not stale. **The public post must never point at the intro as outdated.** Treating the professor's current line as a dated error would be both inaccurate and a bad look on his own board.
- **V11-V13, the fabrication / scaling videos** - Lincoln Lab scientists, clearly recorded in 2018 (several already carry explicit "As of 2018" stamps). These, and only these, are what the public post targets.

## Footnote map (public: Lincoln Lab 2018 videos only)

Source: course transcripts Q1M2V11a to Q1M2V13b (REV_2026, English .srt), read 2026-10-14.

| Video | Time | What it says | Dated? | Proposed footnote |
|---|---|---|---|---|
| V11b | 02:00 | Best coherence times of 100 µs, single-qubit fidelities above 99.9% | No | "2018 figures. Best transmons now reach several hundred µs." |
| V11b | 02:34 | Two-qubit gate fidelities above 99% | No | "2018 figure. Leading devices now report two-qubit fidelities around 99.7% to 99.9%." |
| V12a | 02:11 | Coherence exceeding error-correction thresholds | Yes ("In 2018") | Fine as is |
| V12b | 05:06 | Resonator quality factors | Yes ("As of 2018") | Fine as is |
| **V13a** | **00:00** | **"up to around a few tens of qubits"** | **No** | **"As of 2018. Processors with hundreds to over 1,000 physical qubits exist today."** |
| V13a | 02:36 | Coherence 50 to 100 µs | Yes ("As of 2018") | Fine as is |
| V13b | 04:00 | Plan to scale to "100 qubits or more" | No (future tense) | "Plan as of 2018. That scale has since been exceeded." |

V13a at 00:00 is the highest-priority spot: it opens the scaling video, frames everything after it, and carries no date.

V11a, V12c: no time-sensitive figures needing a stamp (V11a's dilution-fridge note is already phrased as a historical change).

## Remediation options for course staff (cheapest first)

Four tiers, ordered from "anyone can do it today" to "only MIT can do it, and it's hard". The point of the ladder: each tier delivers most of the next tier's value at a fraction of the cost, and Tier 3 is the one worth asking for.

**Tier 1 - Students gather the secondary data (our side of the bargain).**
We collect current public figures from IBM, Google, IonQ, D-Wave: coherence times, gate fidelities, qubit counts, with sources and dates. This is the "newspaper" layer - public, second-hand, and we can do it without troubling anyone at MIT. We hand it over ready to paste.

**Tier 2 - Staff add text/transcript footnotes (platform-native, no footage touched).**
Two edX mechanisms already support this:
- A **Text (HTML) component** placed above or below the video in the unit (Studio > the unit page > Add New Component). Same component type the course already uses elsewhere. Instant, zero editing.
- A **transcript correction**: in the video component, the transcript menu (...) has a Replace option to upload an edited .srt for the same language, and there is now an in-browser transcript editor, so a dated on-screen line can be fixed without the download-edit-reupload round trip. Audio and footage stay untouched.

**Tier 3 - PRIMARY ASK: Lincoln Lab supplies updated first-party data (text only, no filming).**
This is the real value and the whole reason to involve MIT. Everything in Tier 1 is second-hand. Lincoln Lab is an MIT-managed federally funded research and development center (FFRDC), and the V11-V13 presenters are speaking from inside their own 70,000 sq ft microelectronics lab. When a Lincoln Lab scientist states "our devices now reach X coherence", that is a primary measurement from their own machinery - not a citation of someone else's chip. No amount of us scraping press releases reproduces it. The ask is narrow and cheap: a short written update on the current state of their hardware and research (current coherence numbers, where the 3D-stack / TSV / SFQ work went, current wafer and device status). No camera, no re-entering the lab, no disrupting people at work - just their current numbers in text. This gives MIT nearly all the value of fresh footage at almost none of the cost.

**Tier 4 - Fresh footage from the Lab (gold standard, aspirational last resort).**
New video shot inside Lincoln Lab. Highest value, but the hardest: it means a presenter re-entering a working laboratory where real research is ongoing, plus production. The original 2018 presenter may no longer be there. Worth naming as the ideal, but explicitly the last resort precisely because of that difficulty.

Framing for the post: we happily own Tiers 1-2; Tier 3 is what we're really asking MIT for; Tier 4 is the dream, not the demand.

## Private notes - DO NOT raise on the forum

These concern Prof. Oliver's intro (V10), which is current. Challenging the professor's own framing publicly is not worth it. Hold these; raise only through a proper channel if ever, never as a board callout.

- V10 ~01:36: "pushing 1,000 qubits" is fine. IBM Condor crossed 1,121 superconducting qubits in Dec 2023; the field has since prioritized error rates over raw count (IBM Heron, 133 qubits, ~3x lower error). So the number is not stale, it is just no longer the headline metric.
- V10 ~01:49: the intro frames quantum supremacy as a future event reached at ~1,000 qubits. Strictly, supremacy was first claimed by Google in 2019 with a 53-qubit processor. This may be a deliberate pedagogical framing by Oliver rather than an error. Note only; not a public correction.

## References (edX platform mechanics)

- Text components in edX Studio (Add New Component > Text/HTML): https://docs.openedx.org/en/latest/educators/how-tos/course_development/manage_video_transcripts.html and the edX "Working with Text Components" docs.
- Replace/upload an edited .srt transcript for the same language; in-browser transcript editor (frontend-app-authoring PR #3215): https://docs.openedx.org/en/latest/educators/how-tos/course_development/manage_video_transcripts.html

## Notes for verification

- The post itself only proposes date stamps on the 2018 Lincoln Lab videos, so it is safe to publish as is.
- The "today" numbers in the footnote column (coherence of several hundred µs, two-qubit fidelity 99.7% to 99.9%, 1,000+ physical qubits) are from general knowledge, not sources checked on 2026-10-14. Source them before sending the table to course staff.
- **CONFIRMED 2026-10-14:** Lincoln Lab is a federally funded research and development center (FFRDC) MANAGED/OPERATED BY MIT (on behalf of the US defense establishment; cost-reimbursement, no-fee; operating contract held with the US Air Force). Located at Hanscom Air Force Base, Lexington, MA. Public wording to use: "an MIT-managed FFRDC" or "run by MIT" - NOT "part of MIT" (it is not an academic department). Omit the sponsoring-agency name: their own pages are inconsistent (some say Department of Defense, newer ones say U.S. Department of War / DoW). Sources: en.wikipedia.org/wiki/MIT_Lincoln_Laboratory; ll.mit.edu/about/organization/federally-funded-research-and-development-centers; facts.mit.edu/lincoln-laboratory.

## Idea behind it

- Durable content (frameworks, criteria, mechanisms) is the university's job; freshness is the press's job.
- Distinction that keeps the complaint valid: "old" vs "old in a way that builds a wrong mental model".
- Finding from the transcripts: the course already date-stamps some figures; the fix is consistency, not a new practice.
- Secondary data (IBM/Google/IonQ/D-Wave) is the newspaper layer we can supply; Lincoln Lab first-party data is the one input only MIT has.
- Proposal: date-stamp the expiring 2018 figures, don't rewrite the module, don't touch the professor's current intro, and ask Lincoln Lab (an MIT-managed FFRDC) for updated primary data (Tier 3) as the real win.
