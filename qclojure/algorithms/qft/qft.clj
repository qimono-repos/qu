(ns algorithms.qft
  "Quantum Fourier Transform on 3 qubits.

   The QFT transforms a quantum state from the computational basis
   to the frequency (Fourier) basis. It is the quantum analog of the
   discrete Fourier transform and is a key subroutine in Shor's
   algorithm and quantum phase estimation.

   For input |j⟩, the QFT produces:
   |j⟩ → (1/√N) Σ_k e^(2πi·jk/N) |k⟩

   We use the library's built-in QFT circuit and compare with a
   manual implementation to show how QFT rotates phase information."
  (:require [org.soulspace.qclojure.domain.circuit :as qc]
            [org.soulspace.qclojure.application.backend :as qb]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]
            [org.soulspace.qclojure.application.algorithm.quantum-fourier-transform :as qft]))

(defn manual-qft-circuit
  "Build a manual 3-qubit QFT circuit.

   The QFT for n qubits consists of:
   1. For each qubit i (0 to n-1):
      - Apply H to qubit i
      - Apply controlled-Rz(π/2^k) from qubit j to qubit i for j > i
   2. SWAP to reverse qubit order"
  [n]
  (let [circuit (qc/create-circuit n (str "Manual QFT " n "q")
                                   "Hand-built quantum Fourier transform")]
    (-> circuit
        ;; QFT decomposition
        (as-> c
          (reduce (fn [circuit qubit]
                    (let [;; H on current qubit
                          h-c (qc/h-gate circuit qubit)
                          ;; Controlled rotations from later qubits
                          rot-c (reduce (fn [c k]
                                          (let [control (+ qubit k 1)
                                                angle (/ Math/PI (Math/pow 2 (inc k)))]
                                            (if (< control n)
                                              (qc/crz-gate c control qubit angle)
                                              c)))
                                        h-c
                                        (range (- n qubit 1)))]
                      rot-c))
                  c
                  (range n)))
        ;; SWAP to reverse qubit order
        (as-> c
          (reduce (fn [circuit i]
                    (let [j (- n 1 i)]
                      (if (< i j)
                        (qc/swap-gate circuit i j)
                        circuit)))
                  c
                  (range (quot n 2)))))))

(defn -main []
  (println "=== Quantum Fourier Transform (3 qubits) ===")
  (println)
  (println "Input: |1⟩⊗|0⟩⊗|0⟩ = |001⟩ (qubit 0 is |1⟩)")
  (println)
  (let [backend (sim/create-simulator)

        ;; Prepare input state |001⟩ (qubit 0 in |1⟩)
        input-circuit (-> (qc/create-circuit 3 "QFT Input" "Prepare |001⟩")
                          (qc/x-gate 0))
        _ (println "Step 1: Prepare |001⟩ input state")
        (let [r (qb/execute-circuit backend input-circuit {:shots 1024})]
          (doseq [[basis prob] (sort-by key (:probabilities (:final-state r)))]
            (when (> prob 0.001)
              (printf "  |%s⟩  %.4f%n" basis prob))))
        (println)

        ;; QFT using library
        qft-circuit (qft/quantum-fourier-transform-circuit 3)
        full-circuit-1 (-> input-circuit
                           ;; Add QFT gates after the input preparation
                           ;; We need to reconstruct: input then QFT
                           )
        ;; Build full circuit: X(0) then QFT
        full-circuit (-> (qc/create-circuit 3 "QFT on |001⟩" "Full QFT pipeline")
                         (qc/x-gate 0))
        ;; Append QFT operations
        full-circuit (reduce (fn [c op] (assoc c :operations (conj (:operations c) op)))
                             full-circuit
                             (:operations qft-circuit))
        result (qb/execute-circuit backend full-circuit {:shots 1024})]

    (println "Step 2: Apply QFT")
    (println "Final state probabilities (library QFT):")
    (doseq [[basis prob] (sort-by key (:probabilities (:final-state result)))]
      (printf "  |%s⟩  %.4f  (|001⟩ → 1/√8 · Σ e^(2πi·k/8)|k⟩)%n" basis prob))
    (println)
    (println "Expected: QFT|001⟩ produces equal superposition with")
    (println "          different phases for each basis state.")
    (println "          All measurement outcomes should have ≈ 12.5% probability.")
    (println)
    (println "Measurement outcomes:")
    (doseq [[basis n] (sort-by val > (:measurement-results result))]
      (printf "  |%s⟩  %d / 1024 (%.1f%%)%n" basis n (* 100.0 (/ n 1024))))
    result))
