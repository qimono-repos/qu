(ns basic.bloch-sphere
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn print-state [label result]
  (println (str label ":"))
  (doseq [[basis prob] (sort-by key (:probabilities (:final-state result)))]
    (printf "  |%s⟩  %.4f%n" basis prob))
  (println))

(defn -main []
  (println "=== Bloch Sphere — Single-Qubit Rotations ===")
  (println)
  (let [backend (sim/create-simulator)

        north  (qb/execute-circuit backend
                  (qc/create-circuit 1 "State |0⟩" "North pole")
                  {:shots 100})
        _      (print-state "|0⟩ — north pole (Z+)" north)

        south  (qb/execute-circuit backend
                  (-> (qc/create-circuit 1 "X|0⟩" "South pole")
                      (qc/x-gate 0))
                  {:shots 100})
        _      (print-state "X|0⟩ — south pole (|1⟩)" south)

        east   (qb/execute-circuit backend
                  (-> (qc/create-circuit 1 "H|0⟩" "East pole")
                      (qc/h-gate 0))
                  {:shots 100})
        _      (print-state "H|0⟩ — east pole (|+⟩)" east)

        west   (qb/execute-circuit backend
                  (-> (qc/create-circuit 1 "H·X|0⟩" "West pole")
                      (qc/x-gate 0)
                      (qc/h-gate 0))
                  {:shots 100})
        _      (print-state "H·X|0⟩ — west pole (|−⟩)" west)

        ry     (qb/execute-circuit backend
                  (-> (qc/create-circuit 1 "Y·H|0⟩" "Rotate via Y")
                      (qc/h-gate 0)
                      (qc/y-gate 0))
                  {:shots 100})
        _      (print-state "Y·H|0⟩" ry)]

    (println "Bloch sphere poles:")
    (println "  |0⟩  = north (Z+)")
    (println "  |1⟩  = south (Z−)")
    (println "  |+⟩  = east  (X+)")
    (println "  |−⟩  = west  (X−)")))
