(ns classic-circuits.core-test
  (:require [clojure.test :refer [deftest is]
            [classic-circuits.core :as circuit]))

(deftest all-input-pairs-match-integer-multiplication
  (doseq [a (range 4)
          b (range 4)]
    (let [a1 (bit-and (bit-shift-right a 1) 1)
          a0 (bit-and a 1)
          b1 (bit-and (bit-shift-right b 1) 1)
          b0 (bit-and b 1)]
      (is (= (* a b)
             (circuit/bits->int
              (circuit/multiply-2x2-bits a1 a0 b1 b0)))))))

(deftest shared-carry-identity
  (doseq [a1 [0 1], a0 [0 1], b1 [0 1], b0 [0 1]]
    (let [p0 (* a0 b0)
          p1 (* a0 b1)
          p2 (* a1 b0)
          p3 (* a1 b1)]
      (is (= (* p1 p2) (* p0 p3))))))

(deftest non-bits-are-rejected
  (is (thrown? clojure.lang.ExceptionInfo
               (circuit/multiply-2x2-bits 2 0 0 1))))
