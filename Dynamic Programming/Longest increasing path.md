# Longest increasing path

In a grid, start from anywhere end at anywhere, find the longest increasing path.

## Solution

If you look at it strictly from a grid perspective, it starts to look tricky but do a
decomposition of grid to a DAG, and it's immediately obvious what needs to be done.

So you define the edges, build a topo order out of it and then find the longest path
in that DAG.

Here's the nicer bit. If you are forcing an iterative solution, you need to build a dag
to get the iteration order but otherwise, let's say you start at any middle part of the dag,
to compute that you only need to know the NEXT edges, which can be derived on the fly
from the neighbors itself.

Then you can just run that dag compute over all starts and maximise.

A pythonic solution makes it almost the same as the recurrence itself

```python
class Solution:
    def longestIncreasingPath(self, g: list[list[int]]) -> int:
        n, m = len(g), len(g[0])

        def near(i, j):
            return [
                (x, y)
                for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                if 0 <= x < n and 0 <= y < m
            ]

        @cache
        def f(i, j):
            return 1 + max(
                (f(ni, nj) for ni, nj in near(i, j) if g[ni][nj] < g[i][j]), default=0
            )

        return max(f(i, j) for i in range(n) for j in range(m))

```

some python notes

- that default is needed if the list is empty
- that generator wrap is not redundant, apparently it it's not implicity, it's kind of
  like if you were making it a list you would wrap it in `[]`, same for gens
