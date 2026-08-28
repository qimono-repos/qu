;; Shared Guix manifest for all Python workspaces in qu/.
;;
;; Provides Python, uv, and native build deps for wheel compilation,
;; plus the human tooling (TeX engine, docs, editors) used from any
;; workspace. Each workspace's `run` script points here via
;; `guix shell -m ../manifest.scm`.
;;
;; Enter any workspace:
;;   guix shell -m ../manifest.scm
;;   uv sync --python python3
;;
;; Or from the repo root:
;;   guix shell -m manifest.scm
;;
;; Human tooling in this manifest:
;;   tectonic   — self-contained TeX engine for the math/ backbone PDFs
;;   pandoc     — markdown -> HTML/PDF conversion (pipes into tectonic)
;;   vscodium   — libre, telemetry-free VSCode fork
;;   neovim     — terminal-native editor
;;   bat        — syntax-highlighted file preview (markdown too)
;;   tree       — directory tree listing

(specifications->manifest
 (list "python"
        "uv"
        ;; Native bits some wheels still expect when a prebuilt
        ;; package is missing for this exact Python / platform.
        "gcc-toolchain"
        "pkg-config"
        "openssl"
        "zlib"
        ;; Document pipeline: full LaTeX engine + markdown converter.
        "tectonic"
        "pandoc"
        ;; Libre editors.
        "vscodium"
        "neovim"
        ;; Terminal utilities.
        "bat"
        "tree"))
