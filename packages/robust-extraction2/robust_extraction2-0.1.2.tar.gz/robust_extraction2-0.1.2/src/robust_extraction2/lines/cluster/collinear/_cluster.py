from typing import Literal, Unpack, Sequence
from haskellian import iter as I
import numpy as np
from scipy import stats
import networkx as nx
from jaxtyping import Float
from robust_extraction2 import Segments
from .segmentation import segment, SegmentParams
from .metrics import all_pairs, max_proj_dist

def fixed_cluster(
  lines: Segments, M: Float[np.ndarray, 'N N'], *,
  threshold: float,
) -> Sequence[Segments]:
  """Graph-based cluster with fixed `threshold`. Constructs a graph where edges are each pair of segments `(x, y)` with `max_proj_dist(x, y) < threshold`, then finds connected components.
  - `M`: matrix of max projection distances (`M[i][j] == max_proj_dist(lines[i], lines[j])`)
  - `threshold`: max projection distance for two segments to be considered collinear"""
  E = I.transpose(np.where(M < threshold)) # np.where returns a tuple of arrays (one per axis)
  G = nx.Graph(E)
  ccs = list(nx.connected_components(G))
  return [
    lines[list(cc)]
    for cc in ccs
  ]

def segmented_metrics(
  lines: Segments, **params: Unpack[SegmentParams]
) -> Float[np.ndarray, 'N N']:
  """Computes full `N x N` distance metric by splitting the lines across `inclination` in overlapping windows
  - `size`: height or width of the image (if rows or cols)
  """
  buckets = segment(lines, **params)
  bucketed_lines = [lines[b] for b in buckets]
  bucket_metrics = [all_pairs(b, max_proj_dist) for b in bucketed_lines]
  n = len(lines)
  M = np.full((n, n), 1e12)
  for metrics, bucket in zip(bucket_metrics, buckets):
    for i, s1 in enumerate(bucket):
      for j, s2 in enumerate(bucket):
        M[s1, s2] = metrics[i, j]
  return M

def adaptive_cluster(
  lines: Segments, *,
  size: float, min_d: float, min_clusters: int,
  inclination: Literal["horizontal", "vertical"],
  window_size: float | None = None, n_iters: int = 100,
  min_p: float = 0.1, max_p: float = 1.5,
) -> Sequence[Segments]:
  """#### Graph-based, adaptive threshold line cluster
  (as described in [Collinear Segment Clustering v4 (max projection distance + adaptive treshold)](httthresh_proportions://www.notion.so/marcelclaramunt/Collinear-Segment-Clustering-v4-mpd-adaptive-thresh-fb301dc9411c4fafb71926c9e205f472?pvs=4))
  - `size`: height or width (if rows or cols)
  - `inclination`: `horizontal/vertical ->` rows/cols
  - `min_d`: minimum estimated spacing between rows/cols
  - `[min_p, max_p]`: range of proportions of `min_d` to use as thresholds
  - `n_iters`: number of tested thresholds (evenly spaced across `[min_p, max_p]`)
  - `window_size`: size of window whithin which lines are compared for collinearity. Defaults to `2.5*min_d`
  """
  window_size = window_size or 2.5*min_d
  M = segmented_metrics(lines, size=size, inclination=inclination, window_size=window_size)

  cluster_nums = []
  cluster_lens = []
  d = (max_p - min_p) / n_iters
  thresh_proportions = [d*(i+1) + min_p for i in range(n_iters)]
  for p in thresh_proportions:
    clusters = fixed_cluster(lines, M, threshold=min_d*p)
    n = len(clusters)
    ns = [len(c) for c in clusters]
    cluster_nums += [n]
    cluster_lens += [ns]

  feasible_cluster_nums = [n for n in cluster_nums if n >= min_clusters]
  if feasible_cluster_nums == []:
    i = int(np.argmax(cluster_nums))
  else:
    mode = stats.mode(feasible_cluster_nums).mode
    i = int(I.find_last_idx(lambda n: n >= mode, cluster_nums)) # type: ignore

  return fixed_cluster(lines, M, threshold=min_d*thresh_proportions[i])