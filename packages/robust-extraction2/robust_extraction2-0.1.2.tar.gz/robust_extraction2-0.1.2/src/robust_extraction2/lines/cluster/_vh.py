from typing import NamedTuple
import numpy as np
from sklearn.cluster import KMeans
from haskellian import Iter
from robust_extraction2 import lines as ls, Segments

class ClusteredSegments(NamedTuple):
  vlines: Segments
  hlines: Segments

def vh(
  lines: Segments, *,
  h_atol: float = np.deg2rad(8),
  v_atol: float = np.deg2rad(4),
) -> ClusteredSegments:
  """Cluster lines into vertical and horizontal. Returns `vlines, hlines`
  - Clustered by `abs(angle)`, with `angle in [-pi, pi]`
  - `vlines` sorted by `x` s.t.:
    - Each line `[[x1, y1, x2, y2]]` satisfies `x1 < x2`
    - `i <= j` iff `vlines[i][0] <= vlines[j][0]`
  - Similarly, `hlines` sorted by `y`, s.t.:
    - Each line `[[x1, y1, x2, y2]]` satisfies `y1 < y2`
    - `i <= j` iff `hlines[i][1] <= hlines[j][1]`
  """
  angles = np.array([ls.angle(ln) for ln in lines])
  kmeans = KMeans(n_clusters=2, max_iter=5000, n_init=100)
  labs = kmeans.fit_predict(np.abs(angles[:, None]))

  centers = [[alpha], [beta]] = kmeans.cluster_centers_
  v_lab = np.argmax([np.abs(alpha), np.abs(beta)])
  v_angle = centers[v_lab]
  h_angle = centers[1-v_lab]

  vlines = lines[(labs == v_lab) & np.isclose(np.abs(angles), v_angle, atol=v_atol)]
  hlines = lines[(labs == 1-v_lab) & np.isclose(np.abs(angles), h_angle, atol=h_atol)]

  sorted_vlines = np.array(Iter(vlines).map(ls.xsort).sorted(key=lambda ln: ln[0][0]))
  sorted_hlines = np.array(Iter(hlines).map(ls.ysort).sorted(key=lambda ln: ln[0][1]))

  return ClusteredSegments(sorted_vlines, sorted_hlines)