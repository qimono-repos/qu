(ns quantum-circuits.superposition-test
  (:require [clojure.test :refer [deftest is testing]]
            [quantum-circuits.superposition :refer [superposition-stats]]))

(defn- approx= [x y] (< (Math/abs (- (double x) (double y))) 1e-9))

(deftest three-qubits
  (let [{:keys [summands amplitude probability]} (superposition-stats 3)]
    (is (= 8 summands))
    (is (approx= (/ 1.0 (Math/sqrt 8.0)) amplitude))
    (is (approx= (/ 1.0 8) probability))))

(deftest four-qubits
  (let [{:keys [summands amplitude probability]} (superposition-stats 4)]
    (is (= 16 summands))
    (is (approx= 0.25 amplitude))
    (is (approx= (/ 1.0 16) probability))))

(deftest rejects-invalid-n
  (testing "n must be a positive integer"
    (doseq [bad [0 -1 2.0]]
      (is (thrown? clojure.lang.ExceptionInfo (superposition-stats bad))))))
