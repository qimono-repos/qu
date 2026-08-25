(ns examples.bell-state
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn bell-circuit []
  (-> (qc/create-circuit 2 "Bell Circuit" "Creates a Bell state")
      (qc/h-gate 0)
      (qc/cnot-gate 0 1)))

(defn -main []
  (let [circuit  (bell-circuit)
        result   (qb/execute-circuit (sim/create-simulator) circuit {:shots 1000})
        final    (:final-state result)
        meas     (:measurement-results result)]
    (println "Bell circuit created with" (count (:gates circuit)) "gates")
    (println)
    (println "Final state probabilities:")
    (doseq [[basis prob] (sort-by key (:probabilities final))]
      (printf "  |%s⟩  %.4f%n" basis prob))
    (println)
    (println "Measurement outcomes (1000 shots):")
    (doseq [[basis count] (sort-by val > meas)]
      (printf "  |%s⟩  %d (%.1f%%)%n" basis count (* 100.0 (/ count 1000))))
    result))
