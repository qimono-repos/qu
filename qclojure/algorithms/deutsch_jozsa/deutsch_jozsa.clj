(ns algorithms.deutsch-jozsa
  "Deutsch-Jozsa algorithm for n=2 qubits.

   Given a function f: {0,1}^n → {0,1}, determine whether f is
   constant (all 0s or all 1s) or balanced (half 0s, half 1s).

   Classical: requires 2^(n-1)+1 queries in the worst case.
   Quantum:   requires exactly 1 query.

   For n=2 we use 2 input qubits and 1 ancilla (3 total).
   The oracle encodes a balanced function — CNOT from q0 to ancilla."
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(defn dj-balanced-oracle
  "Build a balanced oracle for Deutsch-Jozsa (n=2).

   Encodes f(x0,x1) = x0 (the first input bit).
   This is a balanced function (half the inputs give 0, half give 1).

   The oracle applies CNOT from q0 to the ancilla (q2)."
  [circuit]
  (-> circuit
      (qc/cnot-gate 0 2)))

(defn dj-circuit
  "Build the complete Deutsch-Jozsa circuit for n=2.

   Qubits: q0 (input), q1 (input), q2 (ancilla)
   1. X on ancilla to prepare |1⟩
   2. H on all qubits
   3. Oracle (CNOT from q0 to ancilla)
   4. H on input qubits only
   5. Measure input qubits"
  []
  (-> (qc/create-circuit 3 "Deutsch-Jozsa n=2" "Balanced oracle: f(x)=x0")
      ;; Prepare ancilla in |1⟩
      (qc/x-gate 2)
      ;; H on all qubits
      (qc/h-gate 0)
      (qc/h-gate 1)
      (qc/h-gate 2)
      ;; Apply balanced oracle
      (dj-balanced-oracle)
      ;; H on input qubits
      (qc/h-gate 0)
      (qc/h-gate 1)))

(defn -main []
  (println "=== Deutsch-Jozsa Algorithm (n=2) ===")
  (println)
  (println "Problem: Is f(x0,x1) constant or balanced?")
  (println "Oracle:  f(x0,x1) = x0  (balanced)")
  (println)
  (println "Circuit: X(ancilla) → H(all) → Oracle → H(inputs)")
  (println)
  (let [backend (sim/create-simulator)
        circuit (dj-circuit)
        result  (qb/execute-circuit backend circuit {:shots 1024})]
    (println "Final state probabilities:")
    (doseq [[basis prob] (sort-by key (:probabilities (:final-state result)))]
      (printf "  |%s⟩  %.4f%n" basis prob))
    (println)
    (println "Measurement outcomes (input qubits q0,q1):")
    (doseq [[basis n] (sort-by val > (:measurement-results result))]
      (printf "  |%s⟩  %d%n" basis n))
    (println)
    (println "Interpretation:")
    (println "  If q0,q1 = |00⟩ → function is CONSTANT")
    (println "  If q0,q1 ≠ |00⟩ → function is BALANCED")
    (println)
    (let [freqs (:measurement-results result)
          all-zero? (= (count (filter #(let [[q0 q1 _] (seq (str %))]
                                         (and (= \0 q0) (= \0 q1)))
                                       (keys freqs)))
                       (count (keys freqs)))]
      (if all-zero?
        (println "Result: All outcomes are |00x⟩ → CONSTANT (unexpected)")
        (println "Result: Non-zero outcomes present → BALANCED ✓")))
    result))
