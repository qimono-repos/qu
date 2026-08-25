(ns basic.statevectors
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn -main []
  (println "=== State Vectors ===")
  (println)
  (let [backend (sim/create-simulator)

        zero-circuit (qc/create-circuit 1 "State |0⟩" "Computational basis")
        zero-result  (qb/execute-circuit backend zero-circuit {:shots 1000})
        _            (println "State |0⟩ — probabilities:")
        _            (doseq [[basis prob] (sort-by key (:probabilities (:final-state zero-result)))]
                       (printf "  |%s⟩  %.4f%n" basis prob))

        _            (println)
        plus-circuit (-> (qc/create-circuit 1 "State |+⟩" "Hadamard on |0⟩")
                         (qc/h-gate 0))
        plus-result  (qb/execute-circuit backend plus-circuit {:shots 1000})
        _            (println "State |+⟩ = H|0⟩ — probabilities:")
        _            (doseq [[basis prob] (sort-by key (:probabilities (:final-state plus-result)))]
                       (printf "  |%s⟩  %.4f%n" basis prob))

        _            (println)
        _            (println "Measurement outcomes for |+⟩ (1000 shots):")
        _            (doseq [[basis n] (sort-by key (:measurement-results plus-result))]
                       (printf "  |%s⟩  %d / 1000%n" basis n))
        _            (println)
        _            (println "Note: |+⟩ = (|0⟩ + |1⟩)/√2, so ~50/50 split"))
    plus-result))
