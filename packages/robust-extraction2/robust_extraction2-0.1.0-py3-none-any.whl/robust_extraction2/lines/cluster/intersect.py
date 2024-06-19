from typing import Sequence, Literal
from dataclasses import dataclass
from haskellian import Either, Left, Right
from robust_extraction2 import Segments, Corners, lines as ls

@dataclass
class InsufficientLines:
  axis: Literal['rows', 'cols']
  required: int
  found: int
  detail: str
  tag: Literal['insufficient-lines'] = 'insufficient-lines'

  def __init__(self, axis: Literal['rows', 'cols'], required: int, found: int):
    self.axis = axis
    self.required = required
    self.found = found
    self.detail = f'Found {found} {axis}, but expected {required}'

@dataclass
class ParallelLines:
  detail: str = 'Some extreme gridlines were parallel, thus no intersection could be found. Be proud, this happening is as rare as a UUID collision! (or the picture really sucks)'
  tag: Literal['parallel-lines'] = 'parallel-lines'

IntersectError = InsufficientLines | ParallelLines

def intersect_clusters(
  row_clusters: Sequence[Segments],
  col_clusters: Sequence[Segments]
) -> Either[IntersectError, Corners]:
  if len(row_clusters) < 2:
    return Left(InsufficientLines('rows', required=2, found=len(row_clusters)))
  if len(col_clusters) < 2:
    return Left(InsufficientLines('cols', required=2, found=len(col_clusters)))
  top_eq = ls.cluster.fit_line(row_clusters[0], inclination='rows')
  bot_eq = ls.cluster.fit_line(row_clusters[-1], inclination='rows')
  left_eq = ls.cluster.fit_line(col_clusters[0], inclination='cols')
  right_eq = ls.cluster.fit_line(col_clusters[-1], inclination='cols')
  tl = ls.intersect(top_eq, left_eq)
  tr = ls.intersect(top_eq, right_eq)
  bl = ls.intersect(bot_eq, left_eq)
  br = ls.intersect(bot_eq, right_eq)
  if tl is None or tr is None or bl is None or br is None:
    return Left(ParallelLines())
  return Right(Corners(tl, tr, br, bl))