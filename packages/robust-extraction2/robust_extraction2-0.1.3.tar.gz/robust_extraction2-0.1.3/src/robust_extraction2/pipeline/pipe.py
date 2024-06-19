from typing import NamedTuple, Unpack
from haskellian import either as E
from robust_extraction2 import Img, Contours, ExtendedModel, pipeline as pipe
from .params import Params

Error = pipe.IntersectError | pipe.ExtractionError

class Result(NamedTuple):
  corr_img: Img
  cnts: Contours

@E.do[Error]()
def extract(
  img: Img, model: ExtendedModel, *, autocorrect: bool = True,
  autocorrect_h: int = 1920, autoextract_h: int = 1920,
  **params: Unpack[Params]
):
  if autocorrect:
    corr = pipe.autocorrect(img, model, descale_h=autocorrect_h, **params).unsafe()
  else:
    corr = img
  cnts = pipe.autoextract(corr, model, descale_h=autoextract_h, **params).unsafe()
  return Result(corr, cnts)