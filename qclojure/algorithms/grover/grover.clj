(ns algorithms.grover
  "Grover search on 3 qubits — find |101⟩ (index 5).

   Grover's algorithm searches an unsorted database of N items in
   O(√N) steps instead of the classical O(N).

   For N = 8 items (3 qubits), the optimal number of iterations is:
   ⌊π√8/4⌋ = 2 iterations

   Algorithm:
   1. Initialize uniform superposition |+⟩^⊗3
   2. Repeat 2× (oracle + diffusion):
      a. Oracle: mark target state |101⟩ with phase flip
      b. Diffusion: invert about the average amplitude
   3. Measure — high probability of finding |101⟩"
  (:require [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]
            [org.soulspace.qclojure.application.algorithm.grover :as grover]))

(def target-index
  "Search for |101⟩ which is index 5 in 3-qubit space."
  5)

(defn -main []
  (println "=== Grover Search (3 qubits) ===")
  (println)
  (println "Search space: 8 items (3 qubits)")
  (println "Target: |101⟩ (index 5)")
  (println "Optimal iterations: 2")
  (println)
  (println "Algorithm:")
  (println "  1. H⊗3 — uniform superposition")
  (println "  2. Oracle — phase flip |101⟩")
  (println "  3. Diffusion — amplify target amplitude")
  (println "  4. Repeat steps 2-3 once more")
  (println "  5. Measure — read result with high probability")
  (println)
  (let [backend  (sim/create-simulator)
        result   (grover/grover-algorithm backend 8 #(= % target-index) {:shots 1024})]
    (println "Results:")
    (println "  Algorithm:" (:algorithm result))
    (println "  Success:" (:success result))
    (printf "  Found: |%s⟩ (index %d)%n"
            (format "%3s" (Integer/toString (:result result) 2))
            (:result result))
    (printf "  Probability: %.4f%%%n" (* 100.0 (:probability result)))
    (println "  Iterations:" (:iterations result))
    (println)
    (let [freqs (:frequencies (:measurement-statistics result))]
      (println "Measurement distribution:")
      (doseq [[idx count] (take 5 (sort-by val > freqs))]
        (printf "  |%s⟩  %d / 1024 (%.1f%%)%n"
                (format "%3s" (Integer/toString idx 2))
                count
                (* 100.0 (/ count 1024)))))
    (println)
    (println "Classical search would need ~8 queries on average.")
    (println "Grover found the target in just 2 quantum queries!")))
