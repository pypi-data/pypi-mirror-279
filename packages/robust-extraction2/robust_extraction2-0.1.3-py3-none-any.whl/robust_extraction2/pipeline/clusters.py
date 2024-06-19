from typing import Sequence, Literal
from dataclasses import dataclass
import numpy as np
from haskellian import Either, Left, Right
from robust_extraction2 import Segments, ExtendedModel, match1d, lines as ls

@dataclass
class NotEnoughRows:
  detected: int
  required: int
  reason: Literal['not-enough-rows'] = 'not-enough-rows'

@dataclass
class NotEnoughCols:
  detected: int
  required: int
  reason: Literal['not-enough-cols'] = 'not-enough-cols'

MatchingError = NotEnoughRows | NotEnoughCols

def match_clusters(
  row_clusters: Sequence[Segments], col_clusters: Sequence[Segments],
  *, pen_exp: float = 5, model: ExtendedModel
) -> Either[MatchingError, tuple[Sequence[Segments], Sequence[Segments]]]:
  rows = match1d.invariant(row_clusters, model.rows_template, inclination='rows', pen_exp=pen_exp)
  if rows is None:
    return Left(NotEnoughRows(detected=len(row_clusters), required=model.min_rows))
  cols = match1d.invariant(col_clusters, model.cols_template, inclination='cols', pen_exp=pen_exp)
  if cols is None:
    return Left(NotEnoughCols(detected=len(col_clusters), required=model.min_cols))
  return Right((rows, cols))

def fit_clusters(
  row_clusters: Sequence[Segments], col_clusters: Sequence[Segments],
  *, width: float, height: float,
  method: Literal['ransac', 'least-squares', 'lasso'] = 'least-squares'
):
  fitted_rows = np.array([ls.eq2segment(ls.cluster.fit_line(cluster, method=method, inclination='rows'), x1=0, x2=width) for cluster in row_clusters])
  fitted_cols = np.array([ls.eq2segment(ls.cluster.fit_line(cluster, method=method, inclination='cols'), y1=0, y2=height) for cluster in col_clusters])
  return fitted_rows, fitted_cols