;; Guix development environment for this Cirq workspace.
;;
;; Python and uv come from Guix. Cirq and the rest of the Python
;; stack are then installed into a local virtualenv by uv.
;;
;; Enter the shell:
;;   guix shell -m manifest.scm
;;
;; Then (still inside that shell) create / refresh the venv:
;;   uv sync --python python3
;;
;; Run a script:
;;   uv run python cirq-demo.py
;;
;; Launch notebooks:
;;   uv run jupyter notebook

(specifications->manifest
 (list "python"
       "uv"
       ;; Native bits some wheels still expect when a prebuilt
       ;; package is missing for this exact Python / platform.
       "gcc-toolchain"
       "pkg-config"
       "openssl"
       "zlib"))
