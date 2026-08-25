(ns algorithms.phase-estimation
  "Quantum Phase Estimation (QPE) demonstration.

   QPE estimates the eigenvalue of a unitary operator U given an
   eigenstate |ψ⟩ such that U|ψ⟩ = e^(2πi·φ)|ψ⟩.

   We estimate φ = π/4 using 3 precision qubits.

   Algorithm:
   1. Prepare eigenstate |+⟩ (eigenstate of Z with eigenvalue e^(i·0) or
      we use a controlled-RZ rotation)
   2. Initialize precision qubits in superposition
   3. Apply controlled-U^(2^k) for k = 0..n-1
   4. Apply inverse QFT to precision qubits
   5. Measure precision qubits → read off φ"
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]
            [org.soulspace.qclojure.application.algorithm.quantum-phase-estimation :as qpe]))

(defn -main []
  (println "=== Quantum Phase Estimation ===")
  (println)
  (let [backend   (sim/create-simulator)
        target-phase (/ Math/PI 4)]
    (println "Target phase: π/4 ≈" (format "%.4f" target-phase))
    (println "Precision qubits: 3")
    (println)
    (println "Algorithm steps:")
    (println "  1. Prepare eigenstate qubit (|+⟩)")
    (println "  2. H on 3 precision qubits")
    (println "  3. Controlled-RZ(2^k · φ) for k = 0,1,2")
    (println "  4. Inverse QFT on precision qubits")
    (println "  5. Measure precision qubits")
    (println)

    ;; Run QPE with 3 precision qubits
    (let [result    (qpe/quantum-phase-estimation backend target-phase 3 :plus {:shots 1024})
          estimated (get-in result [:result :estimated-phase])
          actual    (get-in result [:result :actual-phase])
          error     (get-in result [:result :phase-error])
          prob      (get-in result [:result :success-probability])]

      (println "Results:")
      (printf "  Actual phase:    %.4f%n" actual)
      (printf "  Estimated phase: %.4f%n" estimated)
      (printf "  Phase error:     %.4f%n" error)
      (printf "  Success prob:    %.3f%%%n" (* 100.0 prob))
      (println)

      ;; Show top measurement outcomes
      (let [measurements (:measurement-results result)
            freqs (:frequencies measurements)]
        (println "Top measurement outcomes:")
        (doseq [[idx count] (take 5 (sort-by val > freqs))]
          (printf "  Index %d  count %d%n" idx count)))
      (println)

      ;; Compare with different precision levels
      (println "Precision comparison (π/4):")
      (doseq [p [2 3 4]]
        (let [r    (qpe/quantum-phase-estimation backend target-phase p :plus {:shots 1024})
              est  (get-in r [:result :estimated-phase])
              err  (get-in r [:result :phase-error])]
          (printf "  %d qubits: estimated = %.4f  error = %.4f%n" p est err)))
      result)))
