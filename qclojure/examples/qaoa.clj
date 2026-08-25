(ns examples.qaoa
  (:require [org.soulspace.qclojure.application.algorithm.qaoa :as qaoa]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(def c4-graph
  "4-vertex cycle graph: 0-1-2-3-0"
  [[0 1 1.0]
   [1 2 1.0]
   [2 3 1.0]
   [3 0 1.0]])

(defn -main []
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
    (println "MaxCut QAOA on C4 cycle graph")
    (println)
    (println "Algorithm:" (:algorithm result))
    (println "Optimal energy:" (format "%.4f" (:optimal-energy result)))
    (println "Optimal parameters:" (mapv #(format "%.4f" %) (:optimal-parameters result)))
    (println)
    (when-let [ps (:problem-solutions result)]
      (println "Best partition:" (:partition ps))
      (println "Cut edges:    " (:cut-edges ps))
      (println "Cut weight:   " (:cut-weight ps))
      (println "Solution prob:" (format "%.4f" (:solution-probability ps))))
    (println)
    (when-let [ar (:approximation-ratio result)]
      (println "Approximation ratio:" (format "%.4f" ar)))
    result))
