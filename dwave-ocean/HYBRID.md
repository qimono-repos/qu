# Hybrid classical-quantum approach

D-Wave's quantum annealers work in a **hybrid** mode where classical pre-processing
formulates the problem and classical post-processing refines the solution.

## When to use hybrid

| Problem type | Classical role | Quantum role | Example |
|---|---|---|---|
| Combinatorial optimization | Encode as BQM | Quantum annealing | MaxCut, TSP |
| Constraint satisfaction | Reduce constraints | Find low-energy state | Graph coloring |
| Machine learning | Feature engineering | Quantum sampling | QUBO-based ML |

## D-Wave hybrid examples

- `basics/annealing-vs-gate/` — Compare annealing vs gate-model approaches
- `basics/bqm-formulation/` — Formulate problems as binary quadratic models
- `problems/max-cut/` — MaxCut via simulated annealing
- `problems/tsp/` — 4-city TSP via simulated annealing

## Key pattern

D-Wave's approach is **NOT variational** — it's a single-shot anneal:

```
1. Classically encode problem as BQM (Binary Quadratic Model)
2. Submit to quantum annealer (or local simulator)
3. Read out lowest-energy solution
4. Classically decode and verify
```

This differs from gate-model hybrid (QAOA/VQE) where quantum and classical
alternate in a loop. D-Wave does one quantum pass; the "hybrid" is in the
pre/post-processing.
