from typing import Sequence
from haskellian import funcs as F
import cv2 as cv
import numpy as np
from pure_cv import Img
from robust_extraction2 import Contour, Vec2
from ..util import grayscale, adaptive_threshold
from ..rotated_rects import verticalize

def find(img: Img) -> Sequence[Contour]:
  """Find all contours in `img`, by:
  1. Gray scale (if not already so)
  2. Gaussian blur
  3. Threshold
  4. Find Contours
  """
  gray = grayscale(img)
  blurred = cv.GaussianBlur(gray, (5, 5), 0)
  bin_img = adaptive_threshold(blurred)
  contours, _ = cv.findContours(bin_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
  return [c[:, 0, :] for c in contours] # for some reason it returns shape [N, 1, 2] instead of [N, 2]

def filter(contours: Sequence[Contour], min_area: float, max_area: float):
  """Returns all contours `c` s.t. `min_area <= area(c) <= max_area`.
  - If none pass, returns all `c` s.t. `min_area <= area(c)` instead
  """
  big_cnts = [c for c in contours if cv.contourArea(c) >= min_area]
  medium_cnts = [c for c in big_cnts if cv.contourArea(c) <= max_area]
  return medium_cnts if len(medium_cnts) > 0 else big_cnts

def aggregate(contours: Sequence[Contour]) -> cv.typing.RotatedRect:
  """Min. area rotated rect around all `contours`"""
  return F.pipe(contours, np.concatenate, cv.minAreaRect, verticalize)

def inside(p: Vec2, contour: Contour, padding: float = 20) -> bool:
  """Is `p` inside `contour`? (with `padding` tolerance)"""
  return cv.pointPolygonTest(contour, np.float32(p), True) >= -padding # type: ignore