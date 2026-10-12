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
