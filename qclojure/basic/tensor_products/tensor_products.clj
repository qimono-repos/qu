(ns basic.tensor-products
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn -main []
  (println "=== Tensor Products ===")
  (println)
  (let [backend (sim/create-simulator)

        c00 (qb/execute-circuit backend
               (qc/create-circuit 2 "|00⟩" "Two-qubit ground state")
               {:shots 1000})
        _   (println "|0⟩⊗|0⟩ = |00⟩:")
        _   (doseq [[basis prob] (sort-by key (:probabilities (:final-state c00)))]
              (printf "  |%s⟩  %.4f%n" basis prob))
        _   (println)

        c01 (qb/execute-circuit backend
               (-> (qc/create-circuit 2 "|01⟩" "Flip qubit 1")
                   (qc/x-gate 1))
               {:shots 1000})
        _   (println "|0⟩⊗|1⟩ = |01⟩:")
        _   (doseq [[basis prob] (sort-by key (:probabilities (:final-state c01)))]
              (printf "  |%s⟩  %.4f%n" basis prob))
        _   (println)

        cplus (qb/execute-circuit backend
                (-> (qc/create-circuit 2 "|+⟩|0⟩" "Tensor product of |+⟩ and |0⟩")
                    (qc/h-gate 0))
                {:shots 1000})
        _     (println "|+⟩⊗|0⟩ = (|00⟩+|10⟩)/√2:")
        _     (doseq [[basis n] (sort-by key (:measurement-results cplus))]
                (printf "  |%s⟩  %d / 1000%n" basis n))
        _     (println)
        _     (println "Note: qubit 0 is in superposition, qubit 1 stays |0⟩.")
        _     (println "Only |00⟩ and |10⟩ appear (qubit 1 = 0).")]
    cplus))
