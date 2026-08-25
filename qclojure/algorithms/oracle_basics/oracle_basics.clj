(ns algorithms.oracle-basics
  "Oracle basics — a simple oracle marking the |11⟩ state.

   An oracle is a unitary operator that flips the phase of target
   computational basis states. Here we build a 2-qubit oracle that
   applies a Z gate (phase flip) only when both qubits are |1⟩.

   Circuit:  X—X—●—X—X
                  |
                  Z

   The two X gates around qubit 0 and qubit 1 ensure the CZ fires
   only for |11⟩. For all other inputs the net effect is identity."
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn oracle-circuit
  "Build a 2-qubit oracle circuit that marks |11⟩.

   The oracle implements:  |x,y⟩ → (-1)^(x∧y) |x,y⟩
   which is equivalent to a CZ gate on qubits 0 and 1."
  []
  (-> (qc/create-circuit 2 "Oracle |11⟩" "Phase flip for |11⟩ only")
      (qc/cz-gate 0 1)))

(defn -main []
  (println "=== Oracle Basics ===")
  (println)
  (println "Oracle marks |11⟩ with a phase flip (-1).")
  (println "Circuit: CZ(q0, q1)")
  (println)
  (let [backend (sim/create-simulator)
        circuit (oracle-circuit)
        result  (qb/execute-circuit backend circuit {:shots 1024})]
    (println "Final state probabilities:")
    (doseq [[basis prob] (sort-by key (:probabilities (:final-state result)))]
      (printf "  |%s⟩  %.4f%n" basis prob))
    (println)
    (println "Measurement outcomes:")
    (doseq [[basis n] (sort-by val > (:measurement-results result))]
      (printf "  |%s⟩  %d%n" basis n))
    (println)
    (println "The phase flip is invisible to measurement — all four")
    (println("basis states appear with equal probability.")
             "The oracle only matters when combined with interference.")
    result))
