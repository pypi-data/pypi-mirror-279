import cv2 as cv
import numpy as np
import pure_cv as vc
from robust_extraction2 import Segments

def find(
  img: vc.Img, thresholded: bool = False,
  rho: float = 1,
  theta: float = np.pi / 180,
  threshold: int = 100,
  min_length: float = 200,
  max_gap: float = 5
) -> Segments:
  """`cv.HoughLinesP` with good default parameters for Robust Extraction (i.e. moderately high threshold and small min length)"""
  bin_img = img if thresholded else vc.threshold(img)
  return cv.HoughLinesP(
    bin_img, rho=rho, theta=theta, threshold=threshold,
    minLineLength=min_length, maxLineGap=max_gap
  )