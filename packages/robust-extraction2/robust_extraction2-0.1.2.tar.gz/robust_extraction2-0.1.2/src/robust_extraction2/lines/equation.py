from typing import overload
from jaxtyping import Shaped
import numpy as np
from robust_extraction2 import Segment, Segments, Vec2

LineEq = Shaped[np.ndarray, '3']

def intersect(l1: LineEq, l2: LineEq) -> Vec2 | None:
  a1, b1, c1 = l1
  a2, b2, c2 = l2
  A = np.array([[a1, b1], [a2, b2]])
  b = np.array([-c1, -c2])
  try:
    return np.linalg.solve(A, b)
  except np.linalg.LinAlgError:
    ...

def all_intersections(rows: Segments, cols: Segments) -> dict[tuple[int, int], Vec2]:
  """Intersects all row-column pairs. Returnds `D` s.t. `D[i, j]` is the intersection of `rows[i]` and `cols[j]` (if it exists)."""
  row_eqs = [segment2eq(row) for row in rows]
  col_eqs = [segment2eq(col) for col in cols]
  xs = {}
  for i, row in enumerate(row_eqs):
    for j, col in enumerate(col_eqs):
      if (x := intersect(row, col)) is not None:
        xs[i, j] = x
  return xs

def segment2eq(segment: Segment) -> LineEq:
  x1, y1, x2, y2 = segment[0]
  a = y2 - y1
  b = x1 - x2
  c = x2*y1 - x1*y2
  return np.array([a, b, c])

@overload
def eq2segment(line: LineEq, /, *, x1: float, x2: float) -> Segment:
  """
  Line equation ax + by + c = 0 to a segment with endpoints at x-coords `x1` and `x2`.
  - If the line is vertical (`b == 0`), `x1` and `x2` are used as y-coords instead.
  """
@overload
def eq2segment(line: LineEq, /, *, y1: float, y2: float) -> Segment:
  """
  Line equation ax + by + c = 0 to a segment with endpoints at y-coords `y1` and `y2`.
  - If the line is vertical (`b == 0`), `y1` and `y2` are used as x-coords instead.
  """

def eq2segment(line: LineEq, *, x1 = None, x2 = None, y1 = None, y2 = None):
  if x1 is not None and x2 is not None:
    return eq2x(line, x1=x1, x2=x2)
  elif y1 is not None and y2 is not None:
    return eq2y(line, y1=y1, y2=y2)
  else:
    raise ValueError("Either (x1 and x2) or (y1 and y2) must be provided")
      
def eq2x(line: LineEq, *, x1: float, x2: float) -> Segment:
  a, b, c = line
  if b == 0:
    # ax + c = 0 => x = -c/a
    x = -c / a
    return np.array([[x, x1, x, x2]])
  else:
    # ax + by + c = 0 => y = -a/b*x - c/b = m*x + n
    m = -a/b 
    n = -c/b
    y1 = m*x1 + n
    y2 = m*x2 + n
    return np.array([[x1, y1, x2, y2]])
  
def eq2y(line: LineEq, *, y1: float, y2: float) -> Segment:
  a, b, c = line
  if a == 0:
    # by + c = 0 => y = -c/b
    y = -c / b
    return np.array([[y1, y, y2, y]])
  else:
    # ax + by + c = 0 => x = -b/a*y - c/a = m*y + n
    m = -b/a
    n = -c/a
    x1 = m*y1 + n
    x2 = m*y2 + n
    return np.array([[x1, y1, x2, y2]])