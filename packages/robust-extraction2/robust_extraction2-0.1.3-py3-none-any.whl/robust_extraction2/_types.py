from typing import TypeAlias, TypedDict, NotRequired, NamedTuple
from jaxtyping import Shaped
from py_jaxtyping import PyArray
import numpy as np

Img2D: TypeAlias = Shaped[np.ndarray, "w h"]
Img3D: TypeAlias = Shaped[np.ndarray, "w h c"]
Img: TypeAlias = Img2D | Img3D

Contour: TypeAlias = Shaped[np.ndarray, 'N 2']
Contours: TypeAlias = Shaped[np.ndarray, 'N C 2']

Segment: TypeAlias = Shaped[np.ndarray, '1 4']
"""`1 x 4`: `[[x1, x2, y1, y2]]`"""

Segments: TypeAlias = Shaped[np.ndarray, 'N 1 4']
"""`N x 1 x 2`: `[[[x1, x2, y1, y2]], ...]`"""

Vec2: TypeAlias = PyArray[Shaped, float, '2']
Vecs2: TypeAlias = Shaped[np.ndarray, 'N 2']

class Corners(NamedTuple):
  tl: Vec2
  tr: Vec2
  br: Vec2
  bl: Vec2

class Pads(TypedDict):
  l: NotRequired[float]; r: NotRequired[float]
  t: NotRequired[float]; b: NotRequired[float]

class RequiredPads(TypedDict):
  l: float; r: float; t: float; b: float