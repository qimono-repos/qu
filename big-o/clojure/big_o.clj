;; Big-O in Clojure — O(1) and O(log n) quantum operations
;;
;; Run: lein repl
;; user=> (load-file "big_o.clj")

(ns big-o
  (:require [qclojure.quantum :as q]))

(defn measure-one
  "O(1) — Constant time: apply H and measure a single qubit."
  []
  (let [circuit (-> (q/circuit 1)
                    (q/h 0)
                    (q/measure 0))
        results (q/simulate circuit 100)]
    (println "O(1) — Single-qubit H + measure:")
    (println "  Results:" results)
    results))

(defn grover-search
  "O(log n) — Grover search on 3 qubits (N=8), marking |101⟩."
  []
  (let [circuit (-> (q/circuit 3)
                    ;; Initialize uniform superposition
                    (q/h 0) (q/h 1) (q/h 2)
                    ;; Oracle: mark |101⟩
                    (q/x 1)
                    (q/cz 0 2)
                    (q/x 1)
                    ;; Diffusion
                    (q/h 0) (q/h 1) (q/h 2)
                    (q/x 0) (q/x 1) (q/x 2)
                    (q/cz 0 2)
                    (q/x 0) (q/x 1) (q/x 2)
                    (q/h 0) (q/h 1) (q/h 2)
                    ;; Measure
                    (q/measure 0) (q/measure 1) (q/measure 2))
        results (q/simulate circuit 100)]
    (println "\nO(log n) — Grover search (N=8, target |101⟩):")
    (println "  Results:" results)
    results))

(defn -main []
  (println "=== Big-O in Quantum Computing ===")
  (measure-one)
  (grover-search))

;; (-main)
