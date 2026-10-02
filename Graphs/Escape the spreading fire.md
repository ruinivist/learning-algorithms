---
leetcode_url: https://leetcode.com/problems/escape-the-spreading-fire/
---

# Escape the spreading fire

2d grid with 0 = grass, 1 is fire and 2 is a wall. I've at top left (0,0) and need to reach
bottom right. On each move, I can go a grass cell and AFTER I move the fire spreads one unit.
Max number of minutes I can avoid moving and still reach safely?

## Solution

Again one of those reachability problems. Reversing the direction does not buy me much, I need
to know immediately if fire is reached my next cell that I want to go to. To do that, I need
to know the min dist of the grass cell to any of the fire cells.

Now as for how long I can stay, for that the reversal helps a lot, as I can just know for any spot,
at what latest time I must reach it so that I can still make it, including my start which then
concludes the problem. Note that now you want to propogate a "max" and hence need a djikstra.
You can also binary search and do a reachability test.

```python
from collections import deque
import heapq
import math


class Solution:
    def maximumMinutes(self, g: list[list[int]]) -> int:
        n, m = len(g), len(g[0])

        # df[i][j] = minute when fire reaches this cell
        df = [[math.inf] * m for _ in range(n)]
        qf = deque()

        for i in range(n):
            for j in range(m):
                if g[i][j] == 1:
                    qf.append((i, j))
                    df[i][j] = 0

        # Multi-source BFS for fire
        while qf:
            i, j = qf.popleft()

            for ni, nj in (
                (i + 1, j),
                (i - 1, j),
                (i, j - 1),
                (i, j + 1),
            ):
                if not (0 <= ni < n and 0 <= nj < m):
                    continue

                if g[ni][nj] == 2:
                    continue

                if df[ni][nj] != math.inf:
                    continue

                df[ni][nj] = df[i][j] + 1
                qf.append((ni, nj))

        # latest[i][j] =
        # latest absolute time we can stand here and still reach target
        latest = [[-math.inf] * m for _ in range(n)]

        # At the safehouse, arriving exactly when fire arrives is allowed.
        latest[n - 1][m - 1] = df[n - 1][m - 1]

        # We want to propagate the largest "latest arrival" values first.
        # note that now weights are not one, you need a djisktra
        # an alternative is a binary search and then reachability test
        pq = [(-latest[n - 1][m - 1], n - 1, m - 1)]

        while pq:
            neg_time, i, j = heapq.heappop(pq)
            cur = -neg_time

            if cur != latest[i][j]:
                continue

            for ni, nj in (
                (i + 1, j),
                (i - 1, j),
                (i, j - 1),
                (i, j + 1),
            ):
                if not (0 <= ni < n and 0 <= nj < m):
                    continue

                if g[ni][nj] == 2:
                    continue

                # To reach (i,j) at time cur,
                # we must be at (ni,nj) by cur - 1.
                #
                # Also, except for the safehouse, we must beat
                # the fire strictly. Why?
                # case say I reach at time t, and after I make
                # that move, fire spreads to my current cell
                # that is invalid
                #
                # time <= df[ni][nj] - 1
                cand = min(
                    cur - 1,
                    df[ni][nj] - 1,
                )

                if cand > latest[ni][nj]:
                    latest[ni][nj] = cand
                    heapq.heappush(pq, (-cand, ni, nj))

        ans = latest[0][0]

        # No valid path even if we start immediately.
        if ans < 0:
            return -1

        # There exists a path the fire never reaches.
        if ans == math.inf:
            return 10**9

        return int(ans)
```

Had the problem instead needed min numbers of moves to reach ( if possible ), it would like

```python
from collections import deque
import math

class Solution:
    def minimumMoves(self, g: list[list[int]]) -> int:
        n, m = len(g), len(g[0])

        # -------------------------------------------------
        # 1. BFS: ( SAME ) earliest time fire reaches each cell
        # -------------------------------------------------
        fire = [[math.inf] * m for _ in range(n)]
        q = deque()

        for i in range(n):
            for j in range(m):
                if g[i][j] == 1:
                    fire[i][j] = 0
                    q.append((i, j))

        while q:
            i, j = q.popleft()

            for ni, nj in (
                (i + 1, j),
                (i - 1, j),
                (i, j + 1),
                (i, j - 1),
            ):
                if not (0 <= ni < n and 0 <= nj < m):
                    continue

                if g[ni][nj] == 2:       # wall
                    continue

                if fire[ni][nj] != math.inf:
                    continue

                fire[ni][nj] = fire[i][j] + 1
                q.append((ni, nj))

        # -------------------------------------------------
        # 2. BFS: shortest SAFE path for us
        # -------------------------------------------------
        q = deque([(0, 0)])
        dist = [[-1] * m for _ in range(n)]
        dist[0][0] = 0

        while q:
            i, j = q.popleft()
            t = dist[i][j]

            if (i, j) == (n - 1, m - 1):
                return t

            for ni, nj in (
                (i + 1, j),
                (i - 1, j),
                (i, j + 1),
                (i, j - 1),
            ):
                if not (0 <= ni < n and 0 <= nj < m):
                    continue

                if g[ni][nj] == 2:
                    continue

                if dist[ni][nj] != -1:
                    continue

                nt = t + 1

                if (ni, nj) == (n - 1, m - 1):
                    # Safehouse: equality with fire is allowed
                    if nt > fire[ni][nj]:
                        continue
                else:
                    # Normal cell: must beat fire strictly
                    if nt >= fire[ni][nj]:
                        continue

                dist[ni][nj] = nt
                q.append((ni, nj))

        return -1
```
