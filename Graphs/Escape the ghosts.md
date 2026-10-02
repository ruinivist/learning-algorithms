---
leetcode_url: https://leetcode.com/problems/escape-the-ghosts/
---

# Escape the ghosts

2d grid. I start at (0,0) and need to reach target. There are multiple ghosts on the way.
We both move simultaenously and I win if I reach end first.

## Solution

This is one of the simpler ones but the idea is important here.

Had it been say one ghost, you could just say win condition is dist(me,tgt) < dist(ghost,tgt).
If the ghost intercepts me at any point earlier then we can just travel together to the end,
all it does it add the same dist on both sides.

This would be the naive solution, but what if there are multiple ghosts? In an undirected
graph d(a->b) = d(b->a) so you can do a single bfs from the target. If there are multiple
targets you can do multi-src bfs from targets.

What if the graph is directed? then the inverse doesn't hold but you then have to work with the
reversed graph, as d(a->b) = d on reversed(b->a).

That is the core idea of the different approaches, note how clean the reversal makes it.

Now as for THIS specific problem, since it's an inf 2d grid, the shortest is just the manhattan
distance.

```python
class Solution:
    def escapeGhosts(self, ghosts: list[list[int]], t: list[int]) -> bool:
        def dist(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        d_me = dist((0, 0), t)
        d_ghosts = (dist(g, t) for g in ghosts)
        return d_me < min(d_ghosts)
```
