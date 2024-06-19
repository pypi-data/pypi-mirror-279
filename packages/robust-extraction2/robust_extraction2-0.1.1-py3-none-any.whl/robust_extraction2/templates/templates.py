from typing import Sequence, Iterable, Callable
from dataclasses import dataclass
from functools import cached_property
from scoresheet_models import Model
import numpy as np
from robust_extraction2 import Vec2, Contour, Contours

@dataclass
class Template1d:
  offsets: Sequence[float]
  """Offsets normalized to sum 1"""
  a: int
  """Index of first important point"""
  b: int
  """Index after last important point (exclusive)"""

  @cached_property
  def points(self) -> list[float]:
    return list(np.cumsum([0, *self.offsets]))
  
  @property
  def imp_points(self) -> list[float]:
    return self.points[self.a:self.b]
  
  @cached_property
  def min(self) -> float:
    return min(self.offsets)

  @staticmethod
  def extend(offsets: Sequence[float], *, pre: Sequence[float] = [], post: Sequence[float] = []):
    """Extend a sequence of offsets with pre and post offsets, normalizing the result to sum 1."""
    all_offsets = [*pre, *offsets, *post]
    s = sum(all_offsets)
    norm_offsets = [x/s for x in all_offsets]
    return Template1d(norm_offsets, a=len(pre), b=len(pre) + len(offsets) + 1)

class ExtendedModel(Model):
  """A scoresheet model with extra rows/cols to ease matching."""
  pre_row_offsets: Sequence[float] = []
  post_row_offsets: Sequence[float] = []
  pre_col_offsets: Sequence[float] = []
  post_col_offsets: Sequence[float] = []

  @cached_property
  def rows_template(self):
    offsets = [1/self.rows for _ in range(self.rows)]
    return Template1d.extend(offsets, pre=self.pre_row_offsets, post=self.post_row_offsets)
  
  @cached_property
  def cols_template(self):
    return Template1d.extend(self.col_offsets, pre=self.pre_col_offsets, post=self.post_col_offsets)
  
  @cached_property
  def block_indices(self):
    i = 0
    ids = []
    for x in self.columns:
      if x is None:
        ids.append(i)
        i += 2
      else:
        i += 1

    return ids
  
  @property
  def min_rows(self):
    return self.rows + 1
  
  @property
  def min_cols(self):
    return len(self.col_offsets)
  
  @property
  def rmin(self):
    return self.rows_template.min
  
  @property
  def cmin(self):
    return self.cols_template.min

def box_indices(
  rows: list[int],
  block_cols: list[int]
) -> Iterable[tuple[int, int]]:
  """`(row, col)` indices of box top left corners"""
  for c in block_cols:
    for r in rows:
      yield (r, c)
      yield (r, c+1)

def contour(
	row: int, col: int,
	intersect: Callable[[tuple[int, int]], Vec2 | None]
) -> Contour | None:
	tl = intersect((row, col))
	tr = intersect((row, col+1))
	bl = intersect((row+1, col))
	br = intersect((row+1, col+1))
	xs = [tl, tr, br, bl]
	if all(x is not None for x in xs):
		return np.round(xs).astype(int).reshape(4, 1, 2) # type: ignore
   
def contours(
  model: ExtendedModel,
  intersect: Callable[[tuple[int, int]], Vec2 | None]
) -> Contours | None:
  rows = list(range(model.rows))
  contours = []
  for i, j in box_indices(rows, model.block_indices):
    if (cnt := contour(i, j, intersect)) is None:
      return None
    else:
      contours.append(cnt)
  return np.array(contours)
    