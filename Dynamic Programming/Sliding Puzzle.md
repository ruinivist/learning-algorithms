# Sliding Puzzle

2x3 grid where we want to go from state A to B.
Given how small it is, I guess all I need to do is a BFS
till I hit the needed state.
For easy of implementation, a dfs would work just as well. I
just need to put a @cache.

## Solution

```python
from collections import deque
from itertools import chain


class Solution:
    def slidingPuzzle(self, b: list[list[int]]) -> int:
        # ig you can just do a brute force, as long as you
        # don't go in cycles there would be a solution

        q = deque()
        q.append(b)
        dist = {}

        def key(b):
            return tuple(chain.from_iterable(b))

        dist[key(b)] = 0

        while q:
            cb = q.popleft()
            if cb == [[1, 2, 3], [4, 5, 0]]:
                return dist[key(cb)]

            i, j = next(
                (i, j)
                for i, row in enumerate(cb)
                for j, val in enumerate(row)
                if val == 0
            )

            for ni, nj in ((i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1)):
                if ni >= 0 and nj >= 0 and ni < 2 and nj < 3:
                    # IMP: just cb.copy() would not work as it's nested
                    nb = [row[:] for row in cb]
                    nb[ni][nj], nb[i][j] = nb[i][j], nb[ni][nj]
                    if key(nb) not in dist:
                        dist[key(nb)] = dist[key(cb)] + 1
                        q.append(nb)
        return -1
```
