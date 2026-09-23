# Dungeon Game

Grid of numbers, move from top left to bottom right but the problem is health
can't be negative.

I recall from memory the solution is to just start from the end and solve from there.
But let me try to reason why.

I think the argument was that you need the min starting health, which is a function of
min starting health of where you are next turn. If you go other way the max with 0
is not cleanly possible while keeping on state.

Think of what I "need", what is the contribution of this cell, and what min start I can
live with in that case.

```python
class Solution:
    def calculateMinimumHP(self, g: list[list[int]]) -> int:
        n, m = len(g), len(g[0])
        dp = [[math.inf]*m for _ in range(n)]

        # this is just the recurrence written with
        # final state 1
        dp[n-1][m-1] = max(1,1-g[n-1][m-1])

        for i in range(n-1,-1,-1):
            for j in range(m-1,-1,-1):
                if i == n-1 and j == m-1:
                    continue

                need = min(
                    dp[i+1][j] if i+1<n else math.inf,
                    dp[i][j+1] if j+1<m else math.inf
                )
                contri = g[i][j]
                # start + contri >= need
                # start >= need - contri
                dp[i][j] = max(1,need - contri)

        return dp[0][0]
```
