(ns basic.superposition
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn -main []
  (println "=== Superposition ===")
  (println)
  (let [backend (sim/create-simulator)

        h-circuit (-> (qc/create-circuit 1 "H|0⟩" "Single Hadamard")
                      (qc/h-gate 0))
        h-result  (qb/execute-circuit backend h-circuit {:shots 1000})
        _         (println "H|0⟩ = |+⟩ = (|0⟩+|1⟩)/√2:")
        _         (doseq [[basis n] (sort-by key (:measurement-results h-result))]
                    (printf "  |%s⟩  %d / 1000%n" basis n))
        _         (println)

        hh-circuit (-> (qc/create-circuit 1 "HH|0⟩" "Double Hadamard")
                       (qc/h-gate 0)
                       (qc/h-gate 0))
        hh-result  (qb/execute-circuit backend hh-circuit {:shots 1000})
        _          (println "H·H|0⟩ = |0⟩ (H is self-inverse):")
        _          (doseq [[basis n] (sort-by key (:measurement-results hh-result))]
                     (printf "  |%s⟩  %d / 1000%n" basis n))
        _          (println)

        n-circuit (-> (qc/create-circuit 2 "|+⟩|+⟩" "Two-qubit superposition")
                      (qc/h-gate 0)
                      (qc/h-gate 1))
        n-result  (qb/execute-circuit backend n-circuit {:shots 1000})
        _         (println "H⊗H|00⟩ = (|00⟩+|01⟩+|10⟩+|11⟩)/2:")
        _         (doseq [[basis n] (sort-by val > (:measurement-results n-result))]
                    (printf "  |%s⟩  %d / 1000%n" basis n))]
    n-result))
