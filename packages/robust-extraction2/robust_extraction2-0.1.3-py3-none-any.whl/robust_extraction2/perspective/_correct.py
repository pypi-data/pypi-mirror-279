from typing import Unpack
import numpy as np
import cv2 as cv
from robust_extraction2 import Img, Corners, vectors as vec, Pads, RequiredPads

default_pads = RequiredPads(l=0.02, r=0.02, t=0.02, b=0.02)

def unpack(*, l: float, r: float, t: float, b: float):
  return l, r, t, b

def correct(img: Img, corners: Corners, **pads: Unpack[Pads]) -> Img:
  l, r, t, b = unpack(**(default_pads | pads)) # type: ignore
  tl, tr, br, bl = np.array(corners)
  detected_w = int((vec.dist(tl, tr) + vec.dist(bl, br)) / 2)
  detected_h = int((vec.dist(tl, bl) + vec.dist(tr, br)) / 2)
  pad_left = int(detected_w*l); pad_right = int(detected_w*r)
  pad_top = int(detected_h*t); pad_bot = int(detected_h*b)
  w = int(detected_w + pad_left + pad_right)
  h = int(detected_h + pad_top + pad_bot)
  src = np.array([tl, tr, br, bl])
  dst = np.array([[pad_left, pad_top], [w-pad_right, pad_top], [w-pad_right, h-pad_bot], [pad_left, h-pad_bot]])
  M, _ = cv.findHomography(src, dst)
  return cv.warpPerspective(img, M, (w, h)) 

def correct_perspective(img: Img, corners: Corners, **pads: Unpack[Pads]):
    """Correct image perspective
    - `corners`: relative corners (i.e. [1, 1] is the image's bottom right)
    """
    h, w = img.shape[:2]
    rescaled_corners = np.array(corners)*[w, h]
    return correct(img, rescaled_corners, **pads) # type: ignore