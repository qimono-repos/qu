(ns basic.controlled-gates
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn -main []
  (println "=== Controlled Gates ===")
  (println)
  (let [backend (sim/create-simulator)

        cnot0 (qb/execute-circuit backend
                (-> (qc/create-circuit 2 "CNOT ctrl=|0⟩" "No flip")
                    (qc/cnot-gate 0 1))
                {:shots 1000})
        _     (println "CNOT with control=|0⟩:")
        _     (doseq [[basis prob] (sort-by key (:probabilities (:final-state cnot0)))]
                (printf "  |%s⟩  %.4f%n" basis prob))
        _     (println "  → target stays |0⟩ (control is off)")
        _     (println)

        cnot1 (qb/execute-circuit backend
                (-> (qc/create-circuit 2 "CNOT ctrl=|1⟩" "Flip target")
                    (qc/x-gate 0)
                    (qc/cnot-gate 0 1))
                {:shots 1000})
        _     (println "CNOT with control=|1⟩:")
        _     (doseq [[basis prob] (sort-by key (:probabilities (:final-state cnot1)))]
                (printf "  |%s⟩  %.4f%n" basis prob))
        _     (println "  → target flips to |1⟩")
        _     (println)

        cz0 (qb/execute-circuit backend
               (-> (qc/create-circuit 2 "CZ ctrl=|0⟩" "No phase")
                   (qc/cz-gate 0 1))
               {:shots 1000})
        _   (println "CZ with control=|0⟩:")
        _   (doseq [[basis prob] (sort-by key (:probabilities (:final-state cz0)))]
              (printf "  |%s⟩  %.4f%n" basis prob))
        _   (println "  → no phase change (control is off)")
        _   (println)

        cz1 (qb/execute-circuit backend
               (-> (qc/create-circuit 2 "CZ ctrl=|1⟩" "Phase flip")
                   (qc/x-gate 0)
                   (qc/cz-gate 0 1))
               {:shots 1000})
        _   (println "CZ with control=|1⟩:")
        _   (doseq [[basis prob] (sort-by key (:probabilities (:final-state cz1)))]
              (printf "  |%s⟩  %.4f%n" basis prob))
        _   (println "  → phase flip applied to target")]
    cnot1))
