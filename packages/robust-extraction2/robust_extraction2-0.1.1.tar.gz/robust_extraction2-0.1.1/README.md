# Robust Extraction2

> Robust Extraction, rewrited

## Changes w.r.t. Version 1

### Cluster Intersections
- Original: mean intersection of the cartesian product of lines in both clusters
- New: intersection of a fitted line by cluster (regressed on all endpoints)

### ST-Invariant Matching Penalization

Given the number of matched points $N$ and number of minimum points $n_{min}$, the penalization is defined as $1/(N-n_{min}+1)^e$, where $e$ is the "penalization exponent" parameter:

| Original | New |
|----------|-----|
|   $e=0.5$    | $e=5$   |
| ![Original](media/pen0.5.png) | ![New](media/pen5.png) |

Put simply, we basically force matching as many points as possible that don't incur a huge cost.