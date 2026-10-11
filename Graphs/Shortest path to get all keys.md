# Shortest path to get all keys

m x n grid, "." is empty, "#" is wall, "@" is start. Lowercase = key, uppercase = lock.
To walk over a lock, need key. Upto k locks ( one lock, one key ).
Num moves to get all keys.

## Solution

This can be a bfs except I need to encode state, for the same cell, you should also store
what mask of keys you have. Locks don't matter for the state.
As soon as the mask becomes full you can quit.

Overall the problem is simple, just some impl.

```python
from collections import deque


class Solution:
    def shortestPathAllKeys(self, g: list[str]) -> int:
        n, m = len(g), len(g[0])
        si, sj = next((i, j) for i in range(n) for j in range(m) if g[i][j] == "@")

        k = sum(1 for row in g for ch in row if ch.islower())

        q = deque()
        q.append((si, sj, 0))

        d = {}
        d[(si, sj, 0)] = 0

        while q:
            i, j, mask = q.popleft()

            if mask == (1 << k) - 1:
                return d[(i, j, mask)]

            for ni, nj in ((i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1)):
                if ni < 0 or nj < 0 or ni >= n or nj >= m:
                    continue

                ch = g[ni][nj]
                if ch == "#":
                    continue

                if ch.isupper():
                    lock = ord(ch) - ord("A")
                    if not (mask >> lock & 1):
                        continue

                nmask = mask
                if ch.islower():
                    key = ord(ch) - ord("a")
                    nmask = mask | (1 << key)

                d_key = (ni, nj, nmask)
                if d_key not in d:
                    q.append(d_key)
                    d[d_key] = d[(i, j, mask)] + 1

        return -1
```
