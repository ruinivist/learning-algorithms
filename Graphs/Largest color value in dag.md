# Largest color value in dag

In a dag, score of a path is the number of same colored nodes. Find the max possible score.

## Solution

They made the problem desc a bit ugly through that majority wording.

There's only 26 colors, so you can iterate by colors.
You could actually do it like length of longes path in dag except at each node you store all 26 colors
lengths.

I was having some trouble initially writing it without the gt transpose graph

```python
class Solution:
    def largestPathValue(self, col: str, edges: list[list[int]]) -> int:
        n = len(col)
        g = [[] for _ in range(n)]
        gt = [[] for _ in range(n)]

        indeg = [0] * n
        for x, y in edges:
            g[x].append(y)
            gt[y].append(x)
            indeg[y] += 1

        zeros = [i for i in range(n) if indeg[i] == 0]
        topo = []

        while zeros:
            u = zeros.pop()
            topo.append(u)
            for v in g[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    zeros.append(v)

        if len(topo) != n:
            return -1

        dp = [[0] * 26 for _ in range(n)]

        for c in range(26):
            for v in topo:
                dp[v][c] = (1 if ord(col[v]) - ord("a") == c else 0) + max(
                    (dp[prev][c] for prev in gt[v]), default=0
                )

        return max(map(max, dp))
```

This is the idea to do it without the transpose.
When we process current node we expect all prev ones to have already maxxd my value, all I then do is
add 1 if same color.

```python
class Solution:
    def largestPathValue(self, col: str, edges: list[list[int]]) -> int:
        n = len(col)
        g = [[] for _ in range(n)]

        indeg = [0] * n
        for x, y in edges:
            g[x].append(y)
            indeg[y] += 1

        zeros = [i for i in range(n) if indeg[i] == 0]
        topo = []

        while zeros:
            u = zeros.pop()
            topo.append(u)
            for v in g[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    zeros.append(v)

        if len(topo) != n:
            return -1

        dp = [[0] * 26 for _ in range(n)]

        for c in range(26):
            for v in topo:
                dp[v][c] += 1 if ord(col[v]) - ord("a") == c else 0
                for nxt in g[v]:
                    dp[nxt][c] = max(dp[nxt][c], dp[v][c])

        return max(map(max, dp))
```
