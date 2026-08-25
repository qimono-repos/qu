(ns algorithms.phase-kickback
  "Phase kickback demonstration.

   Phase kickback is the key mechanism behind many quantum algorithms
   (Deutsch-Jozsa, Grover, QPE, Shor). When an oracle acts on a
   |−⟩ ancilla qubit, the phase (-1) is 'kicked back' to the
   control qubits.

   We demonstrate this with a CZ gate:
   1. Put qubit 0 in |+⟩ and qubit 1 in |−⟩ = H·X|0⟩
   2. Apply CZ — the phase flip on |11⟩ manifests as a
      global phase on qubit 0, flipping |+⟩ to |−⟩"
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn kickback-circuit
  "Build a phase-kickback circuit using CZ.

   |0⟩ → H →         ─●─   (qubit 0: target of kickback)
   |0⟩ → H → X → ●── ─●─  (qubit 1: |−⟩ ancilla)

   After CZ, qubit 0 ends up in |−⟩ and qubit 1 stays |−⟩."
  []
  (-> (qc/create-circuit 2 "Phase Kickback" "CZ with |−⟩ ancilla")
      ;; Prepare qubit 1 in |−⟩
      (qc/h-gate 1)
      (qc/x-gate 1)
      ;; Prepare qubit 0 in |+⟩
      (qc/h-gate 0)
      ;; Apply CZ — kicks phase from qubit 1 to qubit 0
      (qc/cz-gate 0 1)))

(defn -main []
  (println "=== Phase Kickback ===")
  (println)
  (println "Setup: q0 in |+⟩, q1 in |−⟩")
  (println "After CZ, the phase (-1) on |11⟩ kicks back to q0.")
  (println "Result: q0 becomes |−⟩, q1 stays |−⟩.")
  (println "Final state should be |−⟩⊗|−⟩ = (|00⟩−|01⟩−|10⟩+|11⟩)/2")
  (println)
  (let [backend (sim/create-simulator)
        circuit (kickback-circuit)
        result  (qb/execute-circuit backend circuit {:shots 1024})]
    (println "Final state probabilities:")
    (doseq [[basis prob] (sort-by key (:probabilities (:final-state result)))]
      (printf "  |%s⟩  %.4f%n" basis prob))
    (println)
    (println "Expected: |00⟩ and |11⟩ have + phase,")
    (println "          |01⟩ and |10⟩ have − phase.")
    (println "          All measurement probabilities ≈ 0.25")
    result))
