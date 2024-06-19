from typing import Unpack
import numpy as np
from haskellian import either as E
import pure_cv as vc
from robust_extraction2 import Pads, Img, ExtendedModel, Corners, \
  lines as ls, pipeline as pipe, perspective as pve
from robust_extraction2.lines.cluster import IntersectError
from .params import Params

def detect_corners(img: Img, model: ExtendedModel, **params: Unpack[pipe.Params]):
  rows, cols = pipe.head(img, model, **params)
  return ls.cluster.intersect_clusters(rows, cols)

@E.do[IntersectError]()
def descaled_detect_corners(img: Img, model: ExtendedModel, *, descale_h = 1920, **params: Unpack[pipe.Params]) -> Corners:
  """Detects perspective corners in the descaled image and rescales them back to the original image."""
  s = img.shape[0] / descale_h
  rescaled_img = vc.rescale_h(img, descale_h)
  corners = detect_corners(rescaled_img, model, **params).unsafe()
  rescaled_corners = np.round(s*np.array(corners)).astype(int)
  return Corners(*rescaled_corners)

@E.do[IntersectError]()
def autocorrect(img: Img, model: ExtendedModel, *, descale_h = 1920, **params: Unpack[Params]) -> Img:
  corners = descaled_detect_corners(img, model, descale_h=descale_h, **params).unsafe()
  return pve.correct(img, corners, **params.get('correction_pads', Pads()))