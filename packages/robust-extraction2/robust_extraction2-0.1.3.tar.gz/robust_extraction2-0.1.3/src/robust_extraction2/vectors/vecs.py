import numpy as np
from robust_extraction2 import Vec2

def dist(u: Vec2, v: Vec2) -> float:
  return np.linalg.norm(u-v) # type: ignore

def normalize(v: Vec2) -> Vec2:
  return v / np.linalg.norm(v)