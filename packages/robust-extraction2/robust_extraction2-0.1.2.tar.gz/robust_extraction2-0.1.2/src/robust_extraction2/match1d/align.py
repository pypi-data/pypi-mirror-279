from typing import NamedTuple, Iterable

class Alignment(NamedTuple):
  i: int; j: int; k: int; l: int
  
def alignments(a: int, b: int, n: int, m: int) -> Iterable[Alignment]:
  """All possible `X[i:j]` vs. `Y[k:l]` alignments s.t. `len(X) >= len(Y)`, i.e. `j - i >= l - k`.
  - `(a, b)`: range of required `Y` points to be matched (remaining are optional)
  - `n = len(X)`
  - `m = len(Y)`
  """
  for k in range(0, a+1): # a included
    for l in range(b, m+1): # l is an exclusive index, so m = len(Y) is included
      lmin = l - k
      for i in range(0, n-lmin+1): # n-lmin included
        for j in range(i+lmin, n+1): # j is an exclusive index, so n = len(X) is included
          yield Alignment(i, j, k, l)