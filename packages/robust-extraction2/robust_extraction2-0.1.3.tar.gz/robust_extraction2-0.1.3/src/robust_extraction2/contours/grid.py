from typing import TypedDict, Unpack, NotRequired
import cv2 as cv
import numpy as np
from pure_cv import Img
from robust_extraction2 import Contour
from .contours import find, aggregate, filter

class AreaParams(TypedDict):
  min_area_p: NotRequired[float]
  """Min. area (in proportion to the image's area) to consider a contour. Defaults to 0.1"""
  max_area_p: NotRequired[float]
  """Max. area (in proportion to the image's area) to consider a contour. Defaults to 0.6"""

def find_grid(img: Img, *, min_area_p = 0.1, max_area_p = 0.6) -> cv.typing.RotatedRect | None:
  """Attempts to find the grid zone contour, discarding the whole-sheet contour.
  - May fail (returning `None`) if no suitable contours are found"""
  h, w = img.shape[:2]
  all_cnts = find(img)
  cnts = filter(all_cnts, min_area=min_area_p*w*h, max_area=max_area_p*w*h)
  if len(cnts) > 0:
    return aggregate(cnts)
  
class GridParams(AreaParams):
  pad_h: NotRequired[float]
  """Relative horizontal padding (added on both sides)"""
  pad_v: NotRequired[float]
  """Relative vertical padding (added on both sides)"""

def find_padded_grid(
  img: Img, *, pad_h = 0.1, pad_v = 0.1,
  **kwargs: Unpack[AreaParams]
) -> Contour:
  """Attempts to find the grid zone contour, discarding the whole-sheet contour
  - Let `(w, h)` be the contour's shape, adds `pad_h*h` (or `pad_v*w`) on each side
  - If no suitable contours are found, defaults to a full image contour
  """
  rect = find_grid(img, **kwargs)
  if rect is None:
    h, w = img.shape[:2]
    return np.int32([[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]]) # type: ignore
  else:
    center, (w, h), angle = rect
    xpad = pad_h*w
    ypad = pad_v*h
    box = (center, (w+2*xpad, h+2*ypad), angle)
    return cv.boxPoints(box) # type: ignore