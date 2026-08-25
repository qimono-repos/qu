;; Shared Guix manifest for all Python workspaces in qu/.
;;
;; This manifest provides Python, uv, native build deps, and
;; optional JVM/Clojure tooling.  Each workspace's `run` script
;; points here via `guix shell -m ../manifest.scm`.
;;
;; Enter any workspace:
;;   guix shell -m ../manifest.scm
;;   uv sync --python python3
;;
;; Or from the repo root:
;;   guix shell -m manifest.scm

(specifications->manifest
 (list "python"
        "uv"
        ;; Native bits some wheels still expect when a prebuilt
        ;; package is missing for this exact Python / platform.
        "gcc-toolchain"
        "pkg-config"
        "openssl"
        "zlib"
        ;; JVM — needed for QClojure (Clojure/Leiningen) and future
        ;; Kotlin frontend work.
        "openjdk21"
        "leiningen"
        ;; Rust — needed if building PyQuil/QVM or CUDA-Q from source.
        "rust"
        "cargo"))
