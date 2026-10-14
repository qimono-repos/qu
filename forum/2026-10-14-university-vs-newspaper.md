# Forum post: What's the role of a university, versus a newspaper?

- Course: MIT xPRO QCFx1
- Type: new standalone thread (meta discussion, follow-up to the superconducting module thread)
- Drafted: 2026-10-14, Albert with Claude
- Status: draft, ready to post
- Origin: Albert's question, "are we asking MIT to do the role of the newspapers?"
- Revision: proposal paragraph rewritten after reading the Module 2 transcripts (V11a to V13b)

---

**What's the role of a university, versus a newspaper?**

A lot of us in the superconducting thread (myself included) have been pointing out that the module's numbers are old, and we mean well. But I want to question the framing of our own complaint, because I think we're quietly asking MIT to do a job that was never its job.

When we say "the content is outdated," what we often mean is "it doesn't match this week's headlines." But that's the newspaper's role, not the university's. A newspaper's value is freshness. A university's value is the opposite: teaching the things that stay true long enough to be worth learning. The DiVincenzo criteria in this module are from around 2000, and in 2026 they're still the frame everyone uses to reason about qubits. The interconnect problem, phase kickback, why coherence matters, none of that expires. A course optimized for freshness would actually be worse, because it would chase noise instead of teaching the signal. If MIT rewrote the material every time a new chip shipped, we'd learn press releases, not physics.

So I don't think the module is "outdated" in the way it first looks. The framework is doing exactly what a university should do.

But here's the one place I'd still push, and I think it's a real issue, not just a cosmetic one. There's a difference between a fact being old and a fact being wrong in a way that misleads. The good news is the course already knows how to handle this: V13a says "As of 2018" before its coherence numbers, and V12b does the same for resonator quality factors. The problem is that it isn't consistent. The opening line of V13a, "up to around a few tens of qubits", has no date, and it's the sentence that frames the whole scaling discussion. The same goes for the gate fidelities in V11b and the "100 qubits or more" plan in V13b. So my proposal is narrow: apply the "as of 2018" stamp the course already uses to those few undated figures. That's a footnote, not a subscription. I'm happy to help put the references together if the staff wants a hand.

Curious what others think: where's the line for you between content that's genuinely outdated and content that just isn't today's news?

---

## Footnote map (Module 2 transcripts, video order)

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

## Notes for verification

- The post itself only proposes date stamps, so it is safe to publish as is.
- The "today" numbers in the footnote column (coherence of several hundred µs, two-qubit fidelity 99.7% to 99.9%, 1,000+ physical qubits) are from general knowledge, not sources checked on 2026-10-14. Source them before sending the table to course staff.

## Idea behind it

- Durable content (frameworks, criteria, mechanisms) is the university's job; freshness is the press's job.
- Distinction that keeps the complaint valid: "old" vs "old in a way that builds a wrong mental model".
- Finding from the transcripts: the course already date-stamps some figures; the fix is consistency, not a new practice.
- Proposal: date-stamp the expiring figures, don't rewrite the module.
