from typing import Unpack
from robust_extraction2 import Img, Pads, Contour, Contours
import cv2 as cv

def roi(
  img: Img, contour: Contour, *,
  l = 0.1, r = 0.1, t = 0.15, b = 0.25
) -> Img:
  x, y, w, h = cv.boundingRect(contour)
  top = max(int(y - t*h), 0)
  bot = int(y + (1+b)*h)
  left = max(int(x - l*w), 0)
  right = int(x + (1+r)*w)
  return img[top:bot, left:right]

def boxes(img: Img, contours: Contours, **pads: Unpack[Pads]):
  return [roi(img, cnt, **pads) for cnt in contours]