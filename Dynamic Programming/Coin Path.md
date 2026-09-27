# Coin Path

You have a max jump distance d.
If you land on coins(i) it costs that amount. If it's -1, you can't land there.
Min cost to get to end from 0, along with the path.

## Solution

fairly standard, other than the path reconstruction which is generally not asked

```python
class Solution:
    def cheapestJump(self, coins: List[int], maxJump: int) -> list[int]:
        n = len(coins)
        parent = [-1] * n

        @cache
        def f(i):
            if coins[i] == -1:
                return math.inf
            if i == n - 1:
                return coins[i]

            best = math.inf

            for j in range(i + 1, min(n, i + maxJump + 1)):
                cost = coins[i] + f(j)

                # this is lexo min as you iterate from smaller j
                # don't re-assing on equality
                if cost < best:
                    best = cost
                    parent[i] = j

            return best

        if f(0) == math.inf:
            return []

        ans = []
        i = 0

        while i != -1:
            ans.append(i + 1)
            i = parent[i]

        return ans
```

> in python, x + math.inf == math.inf, you don't need to account for small offsets
