(ns basic.logic-gates
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn run-gate [backend gate-name gate-fn]
  (let [circuit (-> (qc/create-circuit 1 gate-name "Single-qubit gate demo")
                    (gate-fn 0))
        result  (qb/execute-circuit backend circuit {:shots 1000})
        probs   (:probabilities (:final-state result))]
    (println (str "  " gate-name " on |0⟩:"))
    (doseq [[basis prob] (sort-by key probs)]
      (printf "    |%s⟩  %.4f%n" basis prob))
    (println)))

(defn -main []
  (println "=== Logic Gates ===")
  (println)
  (let [backend (sim/create-simulator)]
    (run-gate backend "X (Pauli-X)" qc/x-gate)
    (run-gate backend "Y (Pauli-Y)" qc/y-gate)
    (run-gate backend "Z (Pauli-Z)" qc/z-gate)
    (run-gate backend "H (Hadamard)" qc/h-gate)
    (run-gate backend "S (Phase)"   qc/s-gate)
    (run-gate backend "T (π/8)"    qc/t-gate)

    (println "Gate effects on |0⟩:")
    (println "  X: |0⟩ → |1⟩  (bit flip)")
    (println "  Y: |0⟩ → i|1⟩")
    (println "  Z: |0⟩ → |0⟩  (phase flip, no effect on |0⟩)")
    (println "  H: |0⟩ → |+⟩  (superposition)")
    (println "  S: |0⟩ → |0⟩  (phase gate, no effect on |0⟩)")
    (println "  T: |0⟩ → |0⟩  (π/8 gate, no effect on |0⟩)")))
