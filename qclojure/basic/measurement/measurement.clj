(ns basic.measurement
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn -main []
  (println "=== Measurement ===")
  (println)
  (let [backend (sim/create-simulator)

        z-circuit (-> (qc/create-circuit 1 "Z-basis" "Measure |+⟩ in Z")
                      (qc/h-gate 0))
        z-result  (qb/execute-circuit backend z-circuit {:shots 2000})
        _         (println "Measure |+⟩ in Z-basis (computational):")
        _         (doseq [[basis n] (sort-by key (:measurement-results z-result))]
                    (printf "  |%s⟩  %d / 2000 (%.1f%%)%n"
                            basis n (* 100.0 (/ n 2000))))
        _         (println "  → 50/50 split, as expected for |+⟩")
        _         (println)

        x-circuit (-> (qc/create-circuit 1 "X-basis" "H then measure")
                      (qc/h-gate 0))
        x-result  (qb/execute-circuit backend x-circuit {:shots 2000})
        _         (println "H|0⟩ measured in Z-basis (= |0⟩ in X-basis):")
        _         (doseq [[basis n] (sort-by key (:measurement-results x-result))]
                    (printf "  |%s⟩  %d / 2000 (%.1f%%)%n"
                            basis n (* 100.0 (/ n 2000))))
        _         (println "  → Certainty, because |0⟩ is an eigenstate of the X measurement basis")
        _         (println)

        certainly (qb/execute-circuit backend
                    (-> (qc/create-circuit 1 "Certainty" "X·X|0⟩ = |0⟩")
                        (qc/x-gate 0)
                        (qc/x-gate 0))
                    {:shots 1000})
        _         (println "X·X|0⟩ = |0⟩ (always):")
        _         (doseq [[basis n] (sort-by key (:measurement-results certainly))]
                    (printf "  |%s⟩  %d / 1000%n" basis n))]
    z-result))
