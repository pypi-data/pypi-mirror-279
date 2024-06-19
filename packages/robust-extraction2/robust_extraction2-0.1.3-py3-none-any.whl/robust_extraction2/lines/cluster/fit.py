from typing import Literal, TYPE_CHECKING
from jaxtyping import Shaped
import numpy as np
from robust_extraction2 import Segments, Vec2, Vecs2, lines as ls, vectors as vec
from ..equation import LineEq, segment2eq

def cluster_points(cluster: Segments) -> Shaped[np.ndarray, 'N 2']:
  points = []
  for [[x1, y1, x2, y2]] in cluster:
    points.extend([(x1, y1), (x2, y2)])
  return np.array(points)

def ransac(x: Vecs2, y: Vecs2):
  from sklearn.linear_model import RANSACRegressor
  ransac = RANSACRegressor()
  ransac.fit(x, y)
  slope = ransac.estimator_.coef_[0] # m
  intercept = ransac.estimator_.intercept_ # n
  return slope, intercept

def least_squares(x: Vecs2, y: Vecs2):
  from sklearn.linear_model import LinearRegression
  ransac = LinearRegression()
  ransac.fit(x, y)
  slope = ransac.coef_[0] # m
  intercept = ransac.intercept_ # n
  return slope, intercept

def lasso(x: Vecs2, y: Vecs2):
  from sklearn.linear_model import Lasso
  ransac = Lasso()
  ransac.fit(x, y)
  slope = ransac.coef_[0] # m
  intercept = ransac.intercept_ # n
  return slope, intercept

def regression(x: Vecs2, y: Vecs2, *, method: Literal['ransac', 'least-squares', 'lasso']):
  if method == 'ransac':
    return ransac(x, y)
  elif method == 'least-squares':
    return least_squares(x, y)
  elif method == 'lasso':
    return lasso(x, y)
  else:
    raise ValueError(f'Invalid method: {method}')

def fit_hline_regression(cluster: Segments, method: Literal['ransac', 'least-squares', 'lasso']) -> LineEq:
  """Fit a roughly horizontal line by regressing `y = mx + n` on all endpoints"""
  points = ls.cluster.cluster_points(cluster)
  x = points[:, 0].reshape(-1, 1)
  y = points[:, 1]
  slope, intercept = regression(x, y, method=method)
  a = slope; b = -1; c = intercept
  return np.array([a, b, c])

def fit_vline_regression(cluster: Segments, method: Literal['ransac', 'least-squares', 'lasso']) -> LineEq:
  """Fit a roughly vertical line by regressing `x = my + n` on all endpoints"""
  points = ls.cluster.cluster_points(cluster)
  x = points[:, 1].reshape(-1, 1)
  y = points[:, 0]
  slope, intercept = regression(x, y, method=method)
  a = -1; b = slope; c = intercept
  return np.array([a, b, c])

def fit_line_mean(cluster: Segments) -> LineEq:
  """Fit line by averaging the coefficients of each segment."""
  equations = np.array([segment2eq(segment) for segment in cluster])
  return equations.mean(axis=0)

def fit_line_weighted_mean(cluster: Segments) -> LineEq:
  """Fit line by weighting each segment's coefficients by its length."""
  lengths = np.array([vec.dist(*ls.pq(s)) for s in cluster])
  equations = np.array([segment2eq(segment) for segment in cluster])
  return np.average(equations, axis=0, weights=lengths)

def fit_line(
  cluster: Segments,
  method: Literal['ransac', 'least-squares', 'lasso', 'mean', 'weighted-mean'] = 'ransac',
  *, inclination: Literal['rows', 'cols']
) -> LineEq:
  if method == 'mean':
    return fit_line_mean(cluster)
  elif method == 'weighted-mean':
    return fit_line_weighted_mean(cluster)
  elif inclination == 'rows':
    return fit_hline_regression(cluster, method=method)
  else:
    return fit_vline_regression(cluster, method=method)
    