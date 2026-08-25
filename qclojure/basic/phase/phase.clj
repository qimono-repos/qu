(ns basic.phase
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn -main []
  (println "=== Phase Shifts ===")
  (println)
  (let [backend (sim/create-simulator)

        s-circuit (-> (qc/create-circuit 1 "S gate on |+⟩" "Phase gate")
                      (qc/h-gate 0)
                      (qc/s-gate 0))
        s-result  (qb/execute-circuit backend s-circuit {:shots 1000})
        _         (println "S gate on |+⟩:")
        _         (doseq [[basis prob] (sort-by key (:probabilities (:final-state s-result)))]
                    (printf "  |%s⟩  %.4f%n" basis prob))
        _         (println)

        t-circuit (-> (qc/create-circuit 1 "T gate on |+⟩" "π/8 gate")
                      (qc/h-gate 0)
                      (qc/t-gate 0))
        t-result  (qb/execute-circuit backend t-circuit {:shots 1000})
        _         (println "T gate on |+⟩:")
        _         (doseq [[basis prob] (sort-by key (:probabilities (:final-state t-result)))]
                    (printf "  |%s⟩  %.4f%n" basis prob))
        _         (println)

        z-circuit (-> (qc/create-circuit 1 "Z gate on |+⟩" "Pauli-Z")
                      (qc/h-gate 0)
                      (qc/z-gate 0))
        z-result  (qb/execute-circuit backend z-circuit {:shots 1000})
        _         (println "Z gate on |+⟩:")
        _         (doseq [[basis prob] (sort-by key (:probabilities (:final-state z-result)))]
                    (printf "  |%s⟩  %.4f%n" basis prob))
        _         (println)
        _         (println "Note: S and T add phase but don't change measurement probabilities.")
        _         (println "Z = S² flips the sign of |1⟩ component.")]
    z-result))
