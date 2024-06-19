from typing import Literal, Unpack
from dataclasses import dataclass
from haskellian import either as E, Left
import numpy as np
import pure_cv as vc
from robust_extraction2 import Img, Contours, ExtendedModel, \
  pipeline as pipe, lines as ls, templates as ts
from .clusters import MatchingError
from .params import Params, DEFAULT_PARAMS, RequiredParams

@dataclass
class ContouringError:
  detail: str = 'Some gridlines could not be intersected. This should not happen.'
  tag: Literal['contouring-error'] = 'contouring-error'

ExtractionError = MatchingError | ContouringError

@E.do[ExtractionError]()
def extract_contours(img: Img, model: ExtendedModel, **params: Unpack[Params]) -> Contours:
  p: RequiredParams = { **DEFAULT_PARAMS, **params }
  row_clusters, col_clusters = pipe.head(img, model, **p)
  matched_rows, matched_cols = pipe.match_clusters(row_clusters, col_clusters, model=model, pen_exp=p['pen_exp']).unsafe()
  rows, cols = pipe.fit_clusters(matched_rows, matched_cols, width=img.shape[1], height=img.shape[0], method=p['cluster_fit_method'])
  intersections = ls.all_intersections(rows, cols)
  cnts = ts.contours(model, intersections.get)
  if cnts is None:
    return Left(ContouringError()).unsafe()
  return cnts

@E.do[ExtractionError]()
def autoextract(img: Img, model: ExtendedModel, *, descale_h: int = 1920, **params: Unpack[Params]) -> Contours:
  descaled_img = vc.descale_h(img, target_height=descale_h)
  scale = img.shape[0] / descaled_img.shape[0]
  contours = pipe.extract_contours(descaled_img, model, **params).unsafe()
  return np.round(contours * scale).astype(int)