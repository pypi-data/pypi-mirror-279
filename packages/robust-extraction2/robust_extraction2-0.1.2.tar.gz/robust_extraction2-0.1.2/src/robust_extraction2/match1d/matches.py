from typing import NamedTuple, Sequence, Literal
import numpy as np
from jaxtyping import Float
from scipy.optimize import linear_sum_assignment
from robust_extraction2 import Segments, templates as ts, lines as ls
from .align import alignments, Alignment

class Match(NamedTuple):
  I: list[int]; J: list[int]; cost: float
  alignment: Alignment; cost_matrix: np.ndarray

def scaled_match(
  alignment: Alignment,
  X: Float[np.ndarray, 'N'], Y: Float[np.ndarray, 'M'], *,
  penalization = lambda n_matched: 1,
):
  i, j, k, l = alignment
  Xn = (X[i:j]-X[i]) / (X[j-1]-X[i])
  Yn = (Y[k:l]-Y[k]) / (Y[l-1]-Y[k])
  C = np.abs(Xn[:, None] - Yn)
  I, J = linear_sum_assignment(C)
  n_matched = min(len(I), len(J))
  p = penalization(n_matched)
  cost: float = C[I, J].sum() * p
  return Match(I=I+i, J=J+k, cost=cost, alignment=Alignment(i, j, k, l), cost_matrix=C)

def invariant(
  clusters: Sequence[Segments], template: ts.Template1d, *,
  inclination: Literal['cols', 'rows'], pen_exp: float = 5,
) -> Sequence[Segments] | None:
  """#### Scale- and Translation-invariant 1d match
  (as described in [Row/Column Matching v5 (single-template st-LAP)](https://www.notion.so/marcelclaramunt/Row-Column-Matching-Scoresheet-Templates-v5-single-template-LAP-d65b5eac34fe46eab6f4d92e09dc27a3?pvs=4))
  - `pen_exp` defaulted to `0.5` in the original version
  - Returns `None` if no valid alignments are found (because `len(clusters) < template.b - template.a`)
  """
  axis = 0 if inclination == 'cols' else 1
  a = template.a; b = template.b
  Y = np.array(template.points)
  lmin = b - a
  penalization = lambda N: 1/(N-lmin+1)**pen_exp
  X = np.array([ls.cluster.cluster_points(cluster).mean(axis=0)[axis] for cluster in clusters]) # midpoints
  matches = [
    scaled_match(alignment, X, Y, penalization=penalization)
    for alignment in alignments(a=a, b=b, n=len(X), m=len(Y))
  ]
  if matches:
    best = min(matches, key=lambda match: match.cost)
    k = best.alignment.k
    I_imp = best.I[a-k:][:b-a]
    matched = [clusters[i] for i in I_imp]
    return matched