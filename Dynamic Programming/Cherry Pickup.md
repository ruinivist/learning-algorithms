# Cherry Pickup

A really really really nice problem after a long time!
I had no clue how to even begin with this one.

You have a usual grid with cherries on cells and some cells being blocked.
Go from top left to bottom right AND THEN from bottom right back to top left.
Total number of cherries you can pick up.

## Solution

Step one is to stop resisting and trying to break the problem into two, there are dependent
state, you cannot break them into two.

Second is to not be tempted of a greedy split like pick the best path on the front journey
and then the best one on the return journey, problem is that you will never take a less
bad path based on the assumption that the cherries you missed on the best path would be
taken by the return journey.

Instead of just one player, do the return journey in reverse. So now you have two players,
both starting at top left and moving at the same time.

State can be (r1,c1,r2,c2)
but note that the number of moves is same for both, so r1 + c1 = r2 + c2,
one of the state is derived and can be dropped. We drop c2 here.

![cherry-pickup](./cherry-pickup-two-walkers.gif)

```python
class Solution:
    def cherryPickup(self, grid: list[list[int]]) -> int:
        n, m = len(grid), len(grid[0])

        @cache
        def f(r1, c1, r2):
            c2 = r1 + c1 - r2
            # invalid cases
            # somehow I felt I did not need to include c2 as if the other 3 are
            # correct it would be too but seems not
            if min(r1, c1, r2, c2) < 0 or max(r1 - n, r2 - n, c1 - m, c2 - m) >= 0:
                return -math.inf
            if grid[r1][c1] == -1 or grid[r2][c2] == -1:
                return -math.inf

            # stop case
            if r1 == n - 1 and r2 == n - 1 and c1 == m - 1:
                return grid[r1][c1]

            ans = grid[r1][c1]
            if (r1, c1) != (r2, c2):
                ans += grid[r2][c2]

            ans = ans + max(
                f(r1 + 1, c1, r2),
                f(r1 + 1, c1, r2 + 1),
                f(r1, c1 + 1, r2),
                f(r1, c1 + 1, r2 + 1),
            )

            return ans

        return max(0, f(0, 0, 0))

```
