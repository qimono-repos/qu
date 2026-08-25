(ns examples.grover
  (:require [org.soulspace.qclojure.application.algorithm.grover :as grover]
            [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]))

(def target-state
  "Search for |101⟩ which is index 5 in 3-qubit space."
  5)

(defn -main []
  (let [backend  (sim/create-simulator)
        result   (grover/grover-algorithm backend 8 #(= % target-state) {:shots 1024})]
    (println "Grover search for |101⟩ (index 5) in 8-item space")
    (println)
    (println "Algorithm:" (:algorithm result))
    (println "Success:  " (:success result))
    (println "Result:   " (str "|" (:result result) "⟩"))
    (println "Probability:" (format "%.4f" (:probability result)))
    (println "Iterations:" (:iterations result))
    (println)
    (let [freqs (:frequencies (:measurement-statistics result))]
      (println "Measurement distribution (top 5):")
      (doseq [[idx count] (take 5 (sort-by val > freqs))]
        (printf "  |%s⟩  %d%n" (format "%3s" (Integer/toString idx 2)) count)))))
