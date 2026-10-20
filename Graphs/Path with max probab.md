# Path with max probab

Give undirected graph, and probab of traversal of edges, find max probab across
all paths from a to b.

## Solution

### Prereq: What properties of binary ops do we need to make djikstra work?

Let's call the edge union op as "comb" and the min/max as "relax".

- A union with "comb" MUST NEVER make it more favorable ( per relax )
  - for min path sum, adding edge must never decrease the sum

- "comb" preserves order. If a < b, then same comb on both ends with say c should not
  flip the ordering.

### Now applying to the problem at hand.

The want the max probab, probab along path is multiplication.
Combination should make it less favorable, which is true for probabs as it decreases.
Multiplication also preserves order so we can apply djikstra.

The rest is then straightforward.

```python
class Solution:
    def maxProbability(
        self,
        n: int,
        edges: list[list[int]],
        succProb: list[float],
        start_node: int,
        end_node: int,
    ) -> float:
        # undirected graph, start to end max probab path
        g = [[] for _ in range(n + 1)]
        for (a, b), p in zip(edges, succProb):
            g[a].append((b, p))
            g[b].append((a, p))

        d = [0] * (n + 1)
        d[start_node] = 1
        pq = [(-1, start_node)]

        while pq:
            curd, u = heapq.heappop(pq)
            curd = -curd
            if curd != d[u]:
                continue

            for v, p in g[u]:
                if curd * p > d[v]:
                    d[v] = curd * p
                    heapq.heappush(pq, (-d[v], v))

        return d[end_node]
```
