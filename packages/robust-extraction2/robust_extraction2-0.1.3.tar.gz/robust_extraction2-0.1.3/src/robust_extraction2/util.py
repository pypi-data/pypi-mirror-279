import cv2 as cv
from ._types import Img, Img2D

def grayscale(img: Img) -> Img2D:
  return cv.cvtColor(img, cv.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

def adaptive_threshold(img: Img) -> Img2D:
  """`cv.adaptiveThreshold` with good default parameters
  - Grayscales the images if 3-dimensional
  - Inverts the image before applying the threshold
  """
  gray_img = grayscale(img)
  return cv.adaptiveThreshold(~gray_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, -3)