from typing import TypedDict, Literal
from robust_extraction2 import Pads

class RequiredParams(TypedDict):
  min_height_p: float
  min_width_p: float
  filter_col_coverage: bool
  filter_row_coverage: bool
  min_length_height_p: float
  max_gap_height_p: float
  cluster_iters: int
  correction_pads: Pads
  pen_exp: float
  cluster_fit_method: Literal['ransac', 'least-squares', 'lasso']

class Params(TypedDict, total=False):
  min_height_p: float
  min_width_p: float
  filter_col_coverage: bool
  filter_row_coverage: bool
  min_length_height_p: float
  max_gap_height_p: float
  cluster_iters: int
  correction_pads: Pads
  pen_exp: float
  cluster_fit_method: Literal['ransac', 'least-squares', 'lasso']

DEFAULT_PARAMS = RequiredParams(
  min_height_p=0.5, min_width_p=0.5,
  filter_col_coverage=True, filter_row_coverage=True,
  min_length_height_p=0.05, max_gap_height_p=0.002,
  cluster_iters=100, correction_pads=Pads(), pen_exp=5,
  cluster_fit_method='least-squares',
)