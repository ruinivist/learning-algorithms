---
leetcode_url: https://leetcode.com/problems/shortest-path-visiting-all-nodes/
---

# Shortest path visiting all nodes

~~classic hamiltonian path one~~
actually in this one you CAN revisit the same nodes again, it's not hamiltonian
path.

## Solution

Once again I found myself looking at a cycle in transitions.

> whenever you see a cycle in transition, a dp is just not possible. Don't try to force
> it look for bfs / graph based approach with pruning heuristics.

Even after I did the bfs, I just assumed we don't need any visited state here as we are meant
to be looping, that is fine but you are NOT meant to be looping over the same (mask,j) state.

So this works, if you treat that as your visited.

```python
class Solution:
    def shortestPathLength(self, g: list[list[int]]) -> int:
        n = len(g)
        q = deque()

        visited = set()
        for i in range(n):
            q.append((1 << i, i, 0))
            visited.add((1 << i, i))

        while q:
            mask, i, moves = q.popleft()
            if mask == (1 << n) - 1:
                return moves
            for j in g[i]:
                nmask = mask | (1 << j)
                if (nmask, j) not in visited:
                    visited.add((nmask, j))
                    q.append((nmask, j, moves + 1))
```
