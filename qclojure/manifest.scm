;; Guix manifest for the QClojure workspace.
;;
;; JVM + Clojure tooling only — no Python needed.
;;
;; Usage:
;;   guix shell -m manifest.scm
;;   lein deps
;;   lein repl

(specifications->manifest
 (list "openjdk"
        "leiningen"))
