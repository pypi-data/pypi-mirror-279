from typing import Literal
import numpy as np
from robust_extraction2 import Segment, Vec2, vectors as vec

def pq(line: Segment) -> tuple[Vec2, Vec2]:
  """Segment endpoints (generally refered to as `p` and `q`)"""
  [[x1, y1, x2, y2]] = line
  return np.array([x1, y1]), np.array([x2, y2])

def midpoint(line: Segment) -> Vec2:
  p, q = pq(line)
  return (p+q)/2

def sort(line: Segment, axis: Literal[0, 1]) -> Segment:
  """Sort line endpoints `(p, q)` by a given `axis` (`0 = x, 1 = y`)"""
  p, q = pq(line)
  return line if p[axis] < q[axis] else np.array([[*q, *p]])

def xsort(line: Segment) -> Segment:
  """Sort line endpoints by `x`"""
  return sort(line, axis=0)

def ysort(line: Segment) -> Segment:
  """Sort line endpoints by `y`"""
  return sort(line, axis=1)

def project(x: Vec2, line: Segment) -> Vec2:
  p, q = pq(line)
  t = vec.normalize(q-p)
  return p + t*np.dot(t, x-p)