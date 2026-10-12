# Moonshot

A running note, planted in Week 2. Not a deliverable. A moving target we sharpen as the course goes, and a place to park cross-domain insights before they get lost.

## The flag

The RB-vs-tomography tension comes down to one wall: randomized benchmarking gives a cheap averaged number with no diagnosis, process tomography gives a full diagnosis at a cost that grows exponentially with qubit count. The field treats that wall as fixed. The moonshot question is whether it has to be.

A promising direction: instead of "measure one number" vs "measure everything," use a physically-motivated prior. Measure only the error mechanisms a real chip can actually have (coherent over-rotation, crosstalk, leakage, drift), and spend measurements distinguishing between plausible failures rather than reconstructing every mathematically possible one.

## Albert's edge (the real point)

The angle here isn't a new physics theorem at Week 2. It's the cross-domain lens: Albert comes from serious software engineering. Treat characterization as a resource-allocation problem, a cost-vs-detail design space, something you profile and monitor like production software. Most of the forum treats it as pure physics. That framing is the contribution to keep developing.

## Physics grounding (to deepen across the course)

- Coherent vs incoherent errors. Coherent = wrong-but-still-unitary (90 deg meant, 91 done); accumulates linearly in structured circuits. Incoherent = environment steals info (T1 relaxation, T2 dephasing); tends to wash out. RB's randomization averages coherent errors away, so the errors that dominate a real algorithm are often the ones the benchmark is blind to.
- Dominant culprits on superconducting chips: decoherence (T1/T2, worse for slow gates), crosstalk (correlated, everywhere with fixed couplings), leakage (population escapes to the |2> state outside the computational space, invisible to standard error correction).
- Leakage is the richest thread: it breaks the two-level assumption at the root, so it breaks both the surface code's parity checks and RB's "stays in qubit space" assumption.

## 2026 landscape (course is a review; field has moved)

- Leakage reduction units built into measurement return the transmon to the computational subspace: 98.4% leakage removal without hurting readout fidelity (QuTech, 2026). arXiv:2511.17460
- RB's temporal-correlation blind spot is now a named published weakness: standard RB assumes temporally uncorrelated noise, which real devices violate. Phys. Rev. Research, 2025 (10.1103/r1z5-ycqc)
- Benchmarking survey mapping RB, process tomography, gate set tomography and more by resource cost vs coherent/incoherent/SPAM error coverage; introduces Deterministic Benchmarking to cut the number of runs. Chem. Rev. 2025 (10.1021/acs.chemrev.4c00870) — this is the one that formalizes Albert's cost-vs-detail axis.

## Next steps

- Revisit after the Trapped-Ion and Superconducting case studies, when the physical grounding is strong enough to make the engineering insight sharp instead of hand-wavy.
- Watch for where the course's 2026 review content lags the current literature; log the gaps here.

---

## Thread: stop judging quantum hardware by classical metrics
Added 2026-10-12 (~10:37 UTC−3), Trapped-Ion case study. Commit timestamp is authoritative.

**Source (course video, Case Study: Trapped-Ion Quantum Computers), Dr. Jeremy Sage, MIT Lincoln Laboratory:**

> "The movie shows a particular quantum computing algorithm, and you may think to yourself, this doesn't look like a computer. To that I would say that we are trying to build something that computes in a fundamentally different and transformative way. And with this in mind, I would argue that we shouldn't expect it to look like anything we've ever seen."

**Albert's moment:** while watching, the software instinct kicked in: look for the familiar architecture (server-client, shared bus, a box with a CPU). The quote landed as the counter: the instinct itself is the trap. The mind-blowing part was not a networking analogy but letting go of the expectation that the machine should resemble one.

**Why it matters for the moonshot:** several "drawbacks" are only drawbacks under a classical ruler.
- "Trapped ions are slow" judges them by clock speed. A machine that computes differently is better judged by how many gates you can trust before the state falls apart (coherence × fidelity), where ions are strong.
- "It doesn't scale like chips" assumes scaling means shrinking and copying on a wafer. Ion systems scale differently (moving ions between zones, linking separate traps).
- Same lens applies to benchmarking: RB itself is a classical-style "one number" metric. Part of the flag above is asking which metrics are native to the machine and which are imported habits.

**Tension to keep honest:** the engineering lens is still Albert's edge (resource allocation, cost-vs-detail). The point is not to drop it, but to notice when it smuggles in classical expectations about form and speed. Use the lens for *decisions*, not for *what the machine should look like*.

**Open question to carry forward:** what would a metric designed for the machine, rather than inherited from classical computing, actually measure? Revisit after the superconducting case study, to compare against a modality that *does* look more like a chip.
