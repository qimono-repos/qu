(ns optimization.qaoa.qaoa
  "QAOA for MaxCut on C4 using QClojure.

   Solves the MaxCut problem on a 4-vertex cycle graph (0-1-2-3-0)
   using the Quantum Approximate Optimization Algorithm.

   The QClojure library handles circuit construction, simulation,
   and parameter optimisation internally."
  (:require [org.soulspace.qclojure.application.algorithm.qaoa :as qaoa]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(def c4-graph
  "4-vertex cycle graph as edge list: [src dst weight]"
  [[0 1 1.0]
   [1 2 1.0]
   [2 3 1.0]
   [3 0 1.0]])

(defn -main []
  (println "=== QAOA MaxCut on C4 ===")
  (println "  Graph: 4-vertex cycle 0-1-2-3-0")
  (println "  Edges:" (mapv (fn [[a b w]] [a b w]) c4-graph))
  (println)
  (println "  Running QAOA with 2 layers, Adam optimiser...")
  (println)

  (let [backend (sim/create-simulator)
        result  (qaoa/quantum-approximate-optimization-algorithm
                 backend
                 {:problem-type       :max-cut
                  :problem-instance   c4-graph
                  :num-qubits         4
                  :num-layers         2
                  :optimization-method :adam
                  :max-iterations     80
                  :shots              1024
                  :parameter-strategy :theoretical})]
    (println "  Algorithm:" (:algorithm result))
    (println "  Optimal energy:" (format "%.4f" (:optimal-energy result)))
    (println "  Optimal parameters:"
             (mapv #(format "%.4f" %) (:optimal-parameters result)))
    (println)

    (when-let [ps (:problem-solutions result)]
      (println "  Best partition:" (:partition ps))
      (println "  Cut edges:     " (:cut-edges ps))
      (println "  Cut weight:    " (:cut-weight ps))
      (println "  Solution prob: " (format "%.4f" (:solution-probability ps))))
    (println)

    (when-let [ar (:approximation-ratio result)]
      (println "  Approximation ratio:" (format "%.4f" ar)))
    (println)
    (println "  Optimal cut on C4 is 4 (all edges cut).")
    result))
