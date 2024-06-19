import numpy as np
from robust_extraction2 import Segment

def angle(line: Segment) -> float:
  """Angle in `[-pi/2, pi/2]`"""
  [[x1, y1, x2, y2]] = line
  dx = x2 - x1
  dy = y2 - y1
  return np.arctan(dy/dx) if dx != 0 else np.pi/2