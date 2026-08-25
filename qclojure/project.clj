(defproject qimono-qclojure "0.1.0"
  :description "Functional quantum computing with QClojure"
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [org.soulspace/qclojure "0.24.0"]]
  :profiles {:dev {:dependencies [[org.clojure/test.check "1.1.1"]]}})
