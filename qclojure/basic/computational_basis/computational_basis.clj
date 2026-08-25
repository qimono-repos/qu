(ns basic.computational-basis
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn -main []
  (println "=== Computational Basis States ===")
  (println)
  (let [backend (sim/create-simulator)

        c0  (qc/create-circuit 1 "State |0⟩" "Computational basis")
        r0  (qb/execute-circuit backend c0 {:shots 1000})
        _   (println "Measure |0⟩:")
        _   (doseq [[basis n] (sort-by key (:measurement-results r0))]
              (printf "  |%s⟩  %d / 1000%n" basis n))

        c1  (-> (qc/create-circuit 1 "State |1⟩" "X gate on |0⟩")
                (qc/x-gate 0))
        r1  (qb/execute-circuit backend c1 {:shots 1000})
        _   (println)
        _   (println "Measure |1⟩ (X|0⟩):")
        _   (doseq [[basis n] (sort-by key (:measurement-results r1))]
              (printf "  |%s⟩  %d / 1000%n" basis n))

        c00 (qc/create-circuit 2 "State |00⟩" "Two-qubit ground state")
        r00 (qb/execute-circuit backend c00 {:shots 1000})
        _   (println)
        _   (println "Measure |00⟩:")
        _   (doseq [[basis n] (sort-by key (:measurement-results r00))]
              (printf "  |%s⟩  %d / 1000%n" basis n))

        c11 (-> (qc/create-circuit 2 "State |11⟩" "Both qubits flipped")
                (qc/x-gate 0)
                (qc/x-gate 1))
        r11 (qb/execute-circuit backend c11 {:shots 1000})
        _   (println)
        _   (println "Measure |11⟩ (X⊗X|00⟩):")
        _   (doseq [[basis n] (sort-by key (:measurement-results r11))]
              (printf "  |%s⟩  %d / 1000%n" basis n))]
    r0))
