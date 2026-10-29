# Study Aid Transcription · Process Tomography vs Randomized Benchmarking

Source: Albert's image attachment in the Finale Quiz Slack thread, “Process Tomography vs Randomized Benchmarking Cheat Sheet.png” (2026-10-29). This Markdown file narrates the image so command-line agents that cannot inspect images can use the same study aid. This is a transcription/summary of the supplied graphic, not an official MIT transcript.

## Process Tomography (PT)
**Subtitle:** Full characterization of a quantum process.

- **Goal:** Reconstruct the complete quantum process (quantum channel) for a gate or device. Learn its full error structure, including coherent and incoherent errors such as over-rotations, phase errors, and leakage.
- **What is measured:** Many input states and many measurement bases, to reconstruct output states for the process.
- **Basic idea:** Prepare input states (examples shown: |0⟩, |1⟩, |+⟩, …), apply process 𝓔, then measure in multiple bases (X, Y, Z). Reconstruct the process matrix χ or Pauli transfer matrix R that best explains input-output data.
- **Output/result:** Full process description, typically a χ matrix (process matrix), Pauli transfer matrix R, or Kraus operators. It can show detailed error types, including coherent errors, incoherent errors, and leakage.
- **Resources/scaling:** Requires many different input states and measurements. Number of settings scales rapidly with qubit number; the image gives approximately 4^n input states and measurements for n qubits. It becomes expensive for multi-qubit systems.
- **Sensitivity to SPAM:** Sensitive to state-preparation and measurement (SPAM) errors. Requires good state preparation and measurement calibration.
- **What errors can be seen:** Specific error types, including coherent errors (over-rotations, phase errors), incoherent errors (e.g. depolarizing noise), and leakage to non-computational states.
- **When to use:** When a full diagnostic of the process is needed; useful for debugging, calibration, and understanding error sources; practical for single-qubit or small multi-qubit systems.
- **Key takeaway in the graphic:** Process tomography tells you what the process is, in detail.

## Randomized Benchmarking (RB)
**Subtitle:** Efficient, robust estimation of average gate fidelity.

- **Goal:** Estimate average error rate (average gate fidelity) for a set of gates, e.g. a Clifford group. Obtain a single robust number reflecting typical performance, largely insensitive to SPAM errors.
- **What is measured:** Survival probability after sequences of random gates of varying length.
- **Basic idea:** Apply random sequences from a group (example: Clifford group), append an inverse sequence, measure survival probability, repeat for many sequences, then fit an exponential decay to extract average error rate.
- **Output/result:** Average gate fidelity F_avg or average error rate r. The graphic shows P(m) = A p^m + B and F_avg = (d p + 1)/(d + 1), where p is the decay parameter and d = 2 for a single qubit.
- **Resources/scaling:** Requires many random sequences, but each sequence is easy to implement and analyze. The graphic says it scales efficiently to many qubits and typically uses the Clifford group or variants.
- **Sensitivity to SPAM:** Largely insensitive to SPAM errors. The graphic says SPAM errors are absorbed into fit parameters A and B, not the decay rate p.
- **What errors can be seen:** Gives an average error rate; does not reveal detailed error structure and is not sensitive to whether errors are coherent or incoherent.
- **When to use:** When a quick, robust, scalable measure of gate performance is needed; standard for comparing devices and tracking improvements; widely used in experiments and industry.
- **Key takeaway in the graphic:** Randomized benchmarking tells you how well the process works, on average.

## Comparison cues from the graphic
- PT prioritizes a detailed process description and diagnosis; RB prioritizes a robust average performance metric.
- PT requires varied preparations and measurement bases; RB uses randomized gate sequences and survival-probability decay.
- PT is described as SPAM-sensitive; RB as largely SPAM-insensitive.
- PT reveals detailed error types; RB gives an average error metric.
- The graphic is a supplied study aid. For course-specific claims, compare it with the Week 4 *Programming Tools* transcript, which uses the term **gate-set tomography (GST)** and states that both RB and GST require substantial data and are limited to small quantum systems.
