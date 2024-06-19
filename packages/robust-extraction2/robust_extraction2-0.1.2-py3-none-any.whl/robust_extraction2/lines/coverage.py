from typing import Literal, Sequence
from jaxtyping import Shaped
import numpy as np
from robust_extraction2 import Segments

def union(intervals: Shaped[np.ndarray, 'N 2']) -> float:
  """Total length of union of intervals."""
  if len(intervals) == 0:
      return 0
  sorted_intervals = np.array(intervals)[np.argsort(intervals[:, 0])]
  total_length = 0
  current_end = -np.inf
  for ends in sorted_intervals:
      start = np.min(ends)
      end = np.max(ends)
      if start > current_end:
          total_length += end - start
          current_end = end
      else:
          if end > current_end:
              total_length += end - current_end
              current_end = end
  return total_length

def coverage_filter(
  clusters: Sequence[Segments],
  axis: Literal[0, 1], k: float = 2, min_p: float = 0.7
) -> Sequence[Segments]:
    """Filters line clusters by their coverage of `axis`. Clusters failing both tests are filtered out:
    - `coverage >= mean(coverage) - k*stddev(coverage)`, and
    - `coverage >= min_p*mean(coverage)`"""
    xs = [c[:, 0, [axis, axis+2]] for c in clusters]
    coverage = [union(x) for x in xs]
    m = np.mean(coverage)
    s = np.std(coverage)
    I = np.where((coverage >= m - k*s) | (coverage >= min_p*m))[0]
    return [clusters[i] for i in I]