(ns basic.toffoli
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn -main []
  (println "=== Toffoli (CCX) Gate ===")
  (println)
  (println "Toffoli = controlled-controlled-NOT")
  (println "Flips target only when both controls are |1⟩")
  (println)
  (let [backend (sim/create-simulator)

        r000 (qb/execute-circuit backend
                (-> (qc/create-circuit 3 "CCX |000⟩" "No controls active")
                    (qc/toffoli-gate 0 1 2))
                {:shots 1000})
        _    (println "|000⟩ — both controls = 0:")
        _    (doseq [[basis prob] (sort-by key (:probabilities (:final-state r000)))]
               (printf "  |%s⟩  %.4f%n" basis prob))
        _    (println "  → target stays |0⟩")
        _    (println)

        r100 (qb/execute-circuit backend
                (-> (qc/create-circuit 3 "CCX |100⟩" "One control active")
                    (qc/x-gate 0)
                    (qc/toffoli-gate 0 1 2))
                {:shots 1000})
        _    (println "|100⟩ — one control = 1:")
        _    (doseq [[basis prob] (sort-by key (:probabilities (:final-state r100)))]
               (printf "  |%s⟩  %.4f%n" basis prob))
        _    (println "  → target stays |0⟩ (need both controls)")
        _    (println)

        r110 (qb/execute-circuit backend
                (-> (qc/create-circuit 3 "CCX |110⟩" "Both controls active")
                    (qc/x-gate 0)
                    (qc/x-gate 1)
                    (qc/toffoli-gate 0 1 2))
                {:shots 1000})
        _    (println "|110⟩ — both controls = 1:")
        _    (doseq [[basis prob] (sort-by key (:probabilities (:final-state r110)))]
               (printf "  |%s⟩  %.4f%n" basis prob))
        _    (println "  → target flips to |1⟩!")
        _    (println)

        r111 (qb/execute-circuit backend
                (-> (qc/create-circuit 3 "CCX |111⟩" "XOR behavior")
                    (qc/x-gate 0)
                    (qc/x-gate 1)
                    (qc/x-gate 2)
                    (qc/toffoli-gate 0 1 2))
                {:shots 1000})
        _    (println "|111⟩ — XOR: target = 1⊕1 = 0:")
        _    (doseq [[basis prob] (sort-by key (:probabilities (:final-state r111)))]
               (printf "  |%s⟩  %.4f%n" basis prob))
        _    (println "  → target flips back to |0⟩ (reversible XOR)")
        _    (println)

        _ (println "Toffoli as AND gate:")
        _ (println "  |a,b,0⟩ —CCX—→ |a,b,a∧b⟩")
        _ (println "  Useful for classical logic in quantum circuits.")]
    r110))
