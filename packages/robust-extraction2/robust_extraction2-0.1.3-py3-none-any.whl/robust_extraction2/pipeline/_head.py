from typing import Unpack
from robust_extraction2 import Img, Segments, lines as ls, contours as cs, ExtendedModel
from .params import Params, RequiredParams, DEFAULT_PARAMS

def cropped_lines(img: Img, *, pad_v: float, pad_h: float):
  lns = ls.find(img)
  cnt = cs.find_padded_grid(img, pad_v=pad_v, pad_h=pad_h)
  return ls.crop_all(lns, cnt)

def cluster_lines(
  lines: Segments, *, min_row_h: float, min_col_w: float,
  min_rows: int, min_cols: int, height: int, width: int, cluster_iters: int
):
  """Cluster rows and columns"""
  vlines, hlines = ls.cluster.vh(lines)
  row_clusters = ls.cluster.collinear.adaptive_cluster(
    hlines, min_d=min_row_h, min_clusters=min_rows,
    size=height, inclination='horizontal', n_iters=cluster_iters
  )
  col_clusters = ls.cluster.collinear.adaptive_cluster(
    vlines, min_d=min_col_w, min_clusters=min_cols,
    size=width, inclination='vertical', n_iters=cluster_iters
  )
  return row_clusters, col_clusters

def head(img: Img, model: ExtendedModel, **params: Unpack[Params]):
  """First part of the pipeline, common to both autocorrection and extraction
  1. Find lines cropped to contour
  2. Cluster lines into vertical/horizontal, then into individual rows/columns
  3. Coverage filter
  """
  p = RequiredParams(DEFAULT_PARAMS | params) # type: ignore
  height, width = img.shape[:2]
  MIN_ROW_H = p['min_height_p']*height*model.rmin
  MIN_COL_W = p['min_width_p']*width*model.cmin
  lines = cropped_lines(img, pad_v=model.rmin, pad_h=model.cmin)
  rows, cols = cluster_lines(
    lines, min_row_h=MIN_ROW_H, min_col_w=MIN_COL_W,
    height=height, width=width, cluster_iters=p['cluster_iters'],
    min_rows=model.min_rows, min_cols=model.min_cols
  )
  filtered_rows = ls.coverage_filter(rows, axis=0) if p['filter_row_coverage'] else rows
  inliner_rows = rows if len(filtered_rows) < model.min_rows else filtered_rows
  filtered_cols = ls.coverage_filter(cols, axis=1) if p['filter_col_coverage'] else cols
  inliner_cols = cols if len(filtered_cols) < model.min_cols else filtered_cols
  return inliner_rows, inliner_cols