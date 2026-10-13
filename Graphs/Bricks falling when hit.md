# Bricks falling when hit

A "grid" graph, for each node to be deleted, it also deleted any nodes that ONLY have that node
as the neighbor, find how many will be deleted. Deletions remain.

## Solutution

There are a deletions and a small graph.

How are the stable bricks defined, ones that are in components connected to the roof.
It's easy to answer components sizes based on a DSU but it can't split, we can only merge and hence we
need to process in reverse so the deletion becomes addition.

Note the assymetric nature of deletes. A delete only deletes if there is a cell, so on reverse I cannot
blindly add a cell, I need to check if there was a cell in the first place.
This can be duplicated as well. So one way is to remove dups and remove hits where there was no cell ever.

The implis actually a bit tedious and full of cases to consider.

```python
class Solution:
    def hitBricks(self, grid: list[list[int]], hits: list[list[int]]) -> list[int]:
        # preprocess
        n, m = len(grid), len(grid[0])
        grid_c = [row[:] for row in grid]

        h = []
        for i, j in hits:
            if grid_c[i][j] == 1:
                h.append(True)
                grid_c[i][j] = 0
            else:
                h.append(False)

        # dsu
        def idx(a, b):
            return a * m + b

        par = [-1] * (n * m + 1)

        def root(a):
            if par[a] < 0:
                return a
            par[a] = root(par[a])
            return par[a]

        def merge(a, b):
            a = root(a)
            b = root(b)
            if a == b:
                return False

            sza, szb = -par[a], -par[b]
            if sza < szb:
                a, b = b, a

            par[a] += par[b]
            par[b] = a
            return True

        def size(a):
            return -par[root(a)]

        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        top = n * m

        # Build DSU for the grid after all hits
        for i in range(n):
            for j in range(m):
                if grid_c[i][j] == 0:
                    continue

                if i == 0:
                    merge(top, idx(i, j))

                if i > 0 and grid_c[i - 1][j] == 1:
                    merge(idx(i, j), idx(i - 1, j))

                if j > 0 and grid_c[i][j - 1] == 1:
                    merge(idx(i, j), idx(i, j - 1))

        # Now process hits in reverse
        ans = [0] * len(hits)

        for k in range(len(hits) - 1, -1, -1):
            if not h[k]:
                continue

            i, j = hits[k]

            before = size(top)

            # Restore the brick
            grid_c[i][j] = 1

            if i == 0:
                merge(top, idx(i, j))

            # Connect to existing neighbors
            for dx, dy in dirs:
                x, y = i + dx, j + dy

                if 0 <= x < n and 0 <= y < m:
                    if grid_c[x][y] == 1:
                        merge(idx(i, j), idx(x, y))

            after = size(top)

            ans[k] = max(0, after - before - 1)

        return ans
```
