# Classical circuits in Clojure

Standalone Clojure CLI project using `deps.edn`. **Leiningen is not used.**

## Run

From this directory with Clojure CLI installed:

```bash
clj -M:run
clj -M:test
```

The implementation takes bits in `a1 a0 b1 b0` order and returns `[c3 c2 c1 c0]`. No third-party runtime library is required; the test alias uses the Cognitect test runner.
