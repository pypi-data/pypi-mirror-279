from typing import Sequence
import numpy as np
from shapely.geometry import LineString, Polygon
from robust_extraction2 import Segment, Segments, Contour
from .points import pq

def crop(line: Segment, cnt: Contour) -> Segment | None:
  """Crops a line to a contour"""
  p, q = pq(line)
  line = LineString([p, q])
  poly = Polygon(cnt)
  match list(line.intersection(poly).coords):
    case [p, q]:
      return np.array([[*p, *q]])
    
def crop_all(lines: Segments | Sequence[Segment], cnt: Contour) -> Segments:
  """Crops all lines to a contour, discarding outside lines"""
  return np.array(
    [cropped for line in lines if (cropped := crop(line, cnt)) is not None],
    dtype=np.int32
  )