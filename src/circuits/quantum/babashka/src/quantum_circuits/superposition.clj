(ns quantum-circuits.superposition
  "Equal-superposition stats for n qubits: H^⊗n |0...0>.
  Matrices are plain vectors of row vectors, no dependencies.")

(def ^:private s (/ 1.0 (Math/sqrt 2.0)))

(def H
  "Single-qubit Hadamard."
  [[s s]
   [s (- s)]])

(defn kron
  "Kronecker product A ⊗ B of two matrices."
  [a b]
  (vec (for [ra a, rb b]
         (vec (for [x ra, y rb] (* x y))))))

(defn- approx= [x y] (< (Math/abs (- (double x) (double y))) 1e-9))

(defn superposition-stats
  "Return {:summands :amplitude :probability} for H^⊗n |0...0>."
  [n]
  (when-not (and (int? n) (pos? n))
    (throw (ex-info "n must be an integer >= 1" {:n n})))
  (let [u   (reduce kron (repeat n H))   ; H ⊗ H ⊗ ... (n times)
        psi (mapv first u)                ; first column = H^⊗n |0...0>
        amp (first psi)]
    (when-not (every? #(approx= % amp) psi)
      (throw (ex-info "amplitudes are not all equal" {:psi psi})))
    (when-not (approx= 1.0 (reduce + (map #(* % %) psi)))
      (throw (ex-info "state is not normalized" {:psi psi})))
    {:summands (count psi) :amplitude amp :probability (* amp amp)}))

(defn -main [& args]
  (if-let [n (some-> (first args) parse-long)]
    (let [{:keys [summands amplitude probability]} (superposition-stats n)]
      (println (format "n=%d: summands=%d, amplitude=%.6f, P per outcome=%.6f"
                       n summands amplitude probability)))
    (do (println "usage: bb superposition-stats <n-qubits>")
        (System/exit 2))))
