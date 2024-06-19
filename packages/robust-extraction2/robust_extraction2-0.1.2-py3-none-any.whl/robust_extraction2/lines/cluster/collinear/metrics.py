from typing import Callable
import numpy as np
from jaxtyping import Shaped
from robust_extraction2 import Vec2, Segment, vectors as vec, lines as ls

def all_pairs(
  xs: Shaped[np.ndarray, 'N *M'],
  f: Callable[[Shaped[np.ndarray, '*M'], Shaped[np.ndarray, '*M']], float],
) -> Shaped[np.ndarray, 'N N']:
  n = len(xs)
  M = np.empty((n, n))
  for i in range(n):
    for j in range(i, n):
      M[i, j] = M[j, i] = f(xs[i], xs[j])
  return M

def proj_dist(line: Segment, p: Vec2) -> float:
  q = ls.project(p, line)
  return vec.dist(p, q)

def max_proj_dist(l1: Segment, l2: Segment) -> float:
  """#### Maximum projection distance
  Given `l1 = (p1, q1), l2 = (p2, q2)`, computes max of distances from endpoint to line, i.e:
  >>> max { d(p1, l2), d(q1, l2), d(p2, l1), d(q2, l1) }
  """
  p1, q1 = ls.pq(l1)
  p2, q2 = ls.pq(l2)
  dp2 = proj_dist(l1, p2)
  dq2 = proj_dist(l1, q2)
  dp1 = proj_dist(l2, p1)
  dq1 = proj_dist(l2, q1)
  return max(dp2, dq2, dp1, dq1)