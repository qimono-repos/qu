(ns basic.entanglement
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn -main []
  (println "=== Entanglement — Bell States ===")
  (println)
  (let [backend (sim/create-simulator)

        phi-plus (qb/execute-circuit backend
                   (-> (qc/create-circuit 2 "Φ+" "Bell state |Φ+⟩")
                       (qc/h-gate 0)
                       (qc/cnot-gate 0 1))
                   {:shots 1000})
        _        (println "|Φ+⟩ = (|00⟩+|11⟩)/√2:")
        _        (doseq [[basis prob] (sort-by key (:probabilities (:final-state phi-plus)))]
                   (printf "  |%s⟩  %.4f%n" basis prob))
        _        (println)
        _        (println "Measurement (1000 shots):")
        _        (doseq [[basis n] (sort-by val > (:measurement-results phi-plus))]
                   (printf "  |%s⟩  %d / 1000%n" basis n))
        _        (println "  → Only |00⟩ and |11⟩, never |01⟩ or |10⟩")
        _        (println)

        phi-minus (qb/execute-circuit backend
                    (-> (qc/create-circuit 2 "Φ-" "Bell state |Φ-⟩")
                        (qc/h-gate 0)
                        (qc/cnot-gate 0 1)
                        (qc/z-gate 0))
                    {:shots 1000})
        _         (println "|Φ-⟩ = (|00⟩−|11⟩)/√2:")
        _         (doseq [[basis prob] (sort-by key (:probabilities (:final-state phi-minus)))]
                    (printf "  |%s⟩  %.4f%n" basis prob))
        _         (println)

        psi-plus (qb/execute-circuit backend
                   (-> (qc/create-circuit 2 "Ψ+" "Bell state |Ψ+⟩")
                       (qc/x-gate 0)
                       (qc/h-gate 0)
                       (qc/cnot-gate 0 1))
                   {:shots 1000})
        _        (println "|Ψ+⟩ = (|01⟩+|10⟩)/√2:")
        _        (doseq [[basis prob] (sort-by key (:probabilities (:final-state psi-plus)))]
                   (printf "  |%s⟩  %.4f%n" basis prob))
        _        (println)

        psi-minus (qb/execute-circuit backend
                    (-> (qc/create-circuit 2 "Ψ-" "Bell state |Ψ-⟩")
                        (qc/x-gate 0)
                        (qc/h-gate 0)
                        (qc/cnot-gate 0 1)
                        (qc/z-gate 0))
                    {:shots 1000})
        _         (println "|Ψ-⟩ = (|01⟩−|10⟩)/√2:")
        _         (doseq [[basis prob] (sort-by key (:probabilities (:final-state psi-minus)))]
                    (printf "  |%s⟩  %.4f%n" basis prob))]
    phi-plus))
