---
leetcode_url: https://leetcode.com/problems/sum-of-distances-in-tree/
---

# Sum of distances in tree

arr(i) = sum dist(i,j) for all j

## Solution

I remember this as a classis tree re-rooting problem. There is a dp as well I recall,
which goes via top two paths or something along those lines.

Let's try re-rooting, the idea was simpler there.

```python
class Solution:
    def sumOfDistancesInTree(self, n: int, edges: list[list[int]]) -> list[int]:
        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)

        # sizes
        sz = [0] * n

        def fsz(i, prev):
            sz[i] = 1 + sum(fsz(j, i) for j in g[i] if j != prev)
            return sz[i]

        fsz(0, -1)

        # first answer
        ans0 = 0

        def f0(i, dist, prev):
            nonlocal ans0
            ans0 += dist
            [f0(j, dist + 1, i) for j in g[i] if j != prev]

        f0(0, 0, -1)

        # delta for each way ( "re"-root )
        ans = [0] * n
        ans[0] = ans0

        # now the rest, we move one level down and notice the delta
        # say we moved to u and par was p and we know ans for p as a
        # what nodes increases by 1? all nodes - sz(u)
        # what decrease by 1? sz(u)
        # delta is n - 2*sz(u)

        def f(i, prev):
            ans[i] = ans[prev] + n - 2 * sz[i] if prev != -1 else ans[i]
            [f(j, i) for j in g[i] if j != prev]

        f(0, -1)

        return ans
```

> it's a bit clever looking but note that I needlessly allocate lists at each level
> avoid using this style

also the first two can be done in one dfs, but this is fine.

I was initially mis-remembering but the more harder to do problem on this style is max
instead of sum as there you can't "undo" the max; harder if you don't use diameters idea.
