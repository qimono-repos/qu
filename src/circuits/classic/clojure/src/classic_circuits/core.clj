(ns classic-circuits.core
  (:gen-class))

(defn- require-bit [name value]
  (when-not (and (integer? value) (#{0 1} value) (not (instance? Boolean value)))
    (throw (ex-info (str name " must be integer 0 or 1") {:name name :value value}))))

(defn multiply-2x2-bits
  "Multiply two unsigned 2-bit numbers.
   Inputs: a1 a0 b1 b0, each 0 or 1.
   Returns output bits [c3 c2 c1 c0]."
  [a1 a0 b1 b0]
  (doseq [[name value] [[:a1 a1] [:a0 a0] [:b1 b1] [:b0 b0]]]
    (require-bit name value))
  (let [p0 (* a0 b0)
        p1 (* a0 b1)
        p2 (* a1 b0)
        p3 (* a1 b1)
        ;; Shared product/carry term: fifth AND gate.
        p4 (* p0 p3)
        c0 p0
        c1 (mod (+ p1 p2) 2)
        c2 (mod (+ p4 p3) 2)
        c3 p4]
    [c3 c2 c1 c0]))

(defn bits->int [[c3 c2 c1 c0]]
  (+ (* c3 8) (* c2 4) (* c1 2) c0))

(defn -main [& _]
  (println "2-bit × 2-bit classical multiplier")
  (println " a  b | product | circuit output")
  (doseq [a (range 4)
          b (range 4)]
    (let [a1 (bit-and (bit-shift-right a 1) 1)
          a0 (bit-and a 1)
          b1 (bit-and (bit-shift-right b 1) 1)
          b0 (bit-and b 1)
          bits (multiply-2x2-bits a1 a0 b1 b0)
          result (bits->int bits)]
      (assert (= result (* a b)) {:a a :b b :result result})
      (println (format " %d  %d |    %2d    |     %s"
                       a b result (apply str bits)))))
  (println "PASS: all 16 input pairs match integer multiplication."))
