(ns algorithms.shor
  "Shor's algorithm (simplified) — factor N=15.

   Shor's algorithm factors integers in polynomial time by combining
   classical preprocessing with quantum period finding.

   Steps:
   1. Check if N is even or prime (classical shortcuts)
   2. Choose random a < N with gcd(a,N) = 1
   3. Use quantum period finding to find period r of a^x mod N
   4. If r is even, compute gcd(a^(r/2) ± 1, N) to get factors

   We factor 15 = 3 × 5 using the library's built-in Shor implementation."
  (:require [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]
            [org.soulspace.qclojure.application.algorithm.shor :as shor]))

(defn -main []
  (println "=== Shor's Algorithm ===")
  (println)
  (println "Problem: Factor N = 15")
  (println "Expected: 15 = 3 × 5")
  (println)
  (println "Classical approach: trial division — O(√N)")
  (println "Quantum approach:   period finding — O((log N)^3)")
  (println)
  (let [backend (sim/create-simulator)
        result  (shor/shor-algorithm backend 15)]
    (println "Shor's algorithm results:")
    (println "  N:" (:N result))
    (println "  Success:" (:success result))
    (println "  Factors:" (:factors result))
    (println "  Method:" (:method result))
    (println "  Attempts:" (count (:attempts result)))
    (println)
    (when-let [stats (:statistics result)]
      (println "Statistics:")
      (printf "  Runtime: %d ms%n" (:runtime stats))
      (printf "  Period:  %s%n" (str (:period stats))))
    (println)

    ;; Also try complete factorization
    (println "Complete factorization:")
    (let [complete (shor/complete-factorization backend 15)]
      (printf "  Prime factors of 15: %s%n" (vec (:prime-factors complete)))
      (printf "  Success: %s%n" (:success complete)))
    result))
