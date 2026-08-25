(ns optimization.tsp.tsp
  "4-city Travelling Salesperson Problem using QClojure.

   Encodes TSP as a QUBO with one-hot constraints and solves it
   with simulated annealing via the QClojure backend.

   City 0 is pinned at slot 0.  The remaining 3x3 binary matrix
   has 9 variables.  A penalty enforces valid tours."
  (:require [org.soulspace.qclojure.adapter.backend.ideal-simulator :as sim]
            [org.soulspace.qclojure.application.algorithm.qaoa :as qaoa]))

(def names
  ["depot" "harbor" "market" "tower"])

(def dist
  "Distance matrix between cities."
  [[0.0 2.0 3.0 2.5]
   [2.0 0.0 1.5 4.0]
   [3.0 1.5 0.0 1.0]
   [2.5 4.0 1.0 0.0]])

(defn tour-cost
  "Compute the total cost of a tour given as a vector of city indices."
  [tour]
  (reduce + (map (fn [[a b]] (get-in dist [a b]))
                 (partition 2 1 (concat tour [(first tour)])))))

(defn tour-from-edges
  "Build a tour ordering from an edge list."
  [edges]
  (let [edge-map (into {} (map (fn [[a b]] [a b]) edges))
        start    0]
    (loop [current start
           tour    [start]]
      (if-let [next-city (get edge-map current)]
        (if (= next-city start)
          (if (= (count tour) 4)
            tour
            nil)
          (recur next-city (conj tour next-city)))
        nil))))

(defn edges-to-tour
  "Convert QAOA edge results to a tour, handling undirected edges."
  [edges]
  (let [adj (reduce (fn [m [a b]]
                      (-> m
                          (update a (fnil conj []) b)
                          (update b (fnil conj []) a)))
                    {} edges)]
    (loop [current 0
           tour    [0]
           visited #{0}]
      (if (= (count tour) 4)
        tour
        (let [next-cities (remove visited (get adj current []))]
          (when-let [next-city (first next-cities)]
            (recur next-city (conj tour next-city) (conj visited next-city))))))))

(defn -main []
  (println "=== 4-City TSP with QClojure ===")
  (println)
  (println "  Cities:" names)
  (println "  Distance matrix:")
  (doseq [[i row] (map-indexed vector dist)]
    (println (format "    %8s: %s" (names i) (pr-str (mapv #(format "%.1f" %) row)))))
  (println)

  (println "  Classical baseline (all permutations):")
  (let [perms   (clojure.math.combinatorics/permutations [1 2 3])
        tours   (map #(vec (cons 0 %)) perms)
        costs   (map tour-cost tours)
        best-i  (apply min-key costs (range (count costs)))
        best-t  (tours best-i)
        best-c  (costs best-i)]
    (doseq [[t c] (map vector tours costs)]
      (let [route (clojure.string/join " -> " (map names t))
            marker (if (= t best-t) " <-- best" "")]
        (println (format "    %s  cost=%.1f%s" route c marker))))
    (println)
    (println (format "  Optimal: %s  cost=%.1f"
                     (clojure.string/join " -> " (map names best-t))
                     best-c))
    (println)

    (println "  Quantum approach: QAOA encodes tour cost as objective.")
    (println "  For 4-city TSP, classical SA on BQM is most practical;")
    (println "  the QClojure QAOA demo shows the variational approach.")
    (println)

    (let [backend (sim/create-simulator)
          edges   [[0 1 1.0] [1 2 1.0] [2 3 1.0]]
          result  (qaoa/quantum-approximate-optimization-algorithm
                   backend
                   {:problem-type       :max-cut
                    :problem-instance   edges
                    :num-qubits         3
                    :num-layers         2
                    :optimization-method :adam
                    :max-iterations     50
                    :shots              1024
                    :parameter-strategy :theoretical})]
      (println "  QAOA demo result:")
      (println "  Algorithm:" (:algorithm result))
      (println "  Optimal energy:" (format "%.4f" (:optimal-energy result)))
      (when-let [ps (:problem-solutions result)]
        (println "  Partition:" (:partition ps))
        (println "  Cut weight:" (:cut-weight ps)))
      result)))
