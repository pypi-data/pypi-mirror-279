from typing import Sequence, Literal, TypedDict
from jaxtyping import Shaped, Bool
import numpy as np
from robust_extraction2 import Segments

def overlapping_windows(d: float, n: int) -> Shaped[np.ndarray, '2*n-1 2']:
  """Ranges `[[0, d], [0.5*d, 1.5*d], [d, 2*d], [1.5*d, 2.5*d], ..., [(n-2)*d, (n-1)]]`
  - `n`: num of non-overlapped windows (total is `2*n - 1`)
  """
  windows = [np.array([0, d])]
  for i in range(1, n):
    w = np.array([i*d, (i+1)*d])
    w2 = w - d/2
    windows += [w2, w]
  return np.array(windows)

def inside(xs: Shaped[np.ndarray, '_ 1'], window: Shaped[np.ndarray, '2']) -> Bool[np.ndarray, '_ 1']:
  return (window[0] <= xs) & (xs <= window[1])

def classify(intervals: Shaped[np.ndarray, '_ 2'], windows: Shaped[np.ndarray, '_ 2']) -> Sequence[Sequence[int]]:
  """Classifies `intervals` into `windows`.
  - Returns sets of indices of `intervals` that intersect with a same window
  - Empty windows are skipped
  """
  xs1 = intervals[:, 0]
  xs2 = intervals[:, 1]
  buckets = [np.where(inside(xs1, window) | inside(xs2, window))[0] for window in windows]
  return [bucket for bucket in buckets if len(bucket) > 0] # type: ignore

class SegmentParams(TypedDict):
  window_size: float
  size: float
  inclination: Literal['vertical', 'horizontal']

def segment(
  lines: Segments, *,
  window_size: float, size: float,
  inclination: Literal['vertical', 'horizontal']
) -> Sequence[Sequence[int]]:
    """Segment lines by windows of `window_size` height/width. Each segment is a set of line indices.
    - `size`: size of the image (height or width) (i.e. of the interval to segment across)
    """
    n_windows = int(np.ceil(size/window_size))
    windows = overlapping_windows(window_size, n_windows)
    # vertical lines are clustered by x; horizontal by y
    xs = lines[:, 0, [0, 2]] if inclination == 'vertical' else lines[:, 0, [1, 3]]
    return classify(xs, windows)