# Paint House II

## Problem

You are given n houses and k colors. costs[i][j] is the cost of painting house i with color j.
If not tow adjance houses can have the same color, min cost to pain all.

## Solution

A straightforward recurrence is just

```
dp[i][j] =
    costs[i][j] +
    min(dp[i-1][c]) for every c != j
```

But for the "previous" i-1 state, if you keep track of top two smallest values, you can
avoid an iteration loop.

Also note that only i and i-1 rows are used so you can collapse that to just two as well.

```python
def minCostII(costs):
    n, k = len(costs), len(costs[0])
    # note the base case
    prev = costs[0][:]

    for i in range(1, n):

        # Find smallest and second-smallest values in prev
        min1 = float('inf')
        min2 = float('inf')
        min_color = -1

        for color in range(k):
            if prev[color] < min1:
                min2 = min1
                min1 = prev[color]
                min_color = color

            elif prev[color] < min2:
                min2 = prev[color]

        curr = [0] * k

        # Compute DP values for current house
        for color in range(k):
            if color == min_color:
                curr[color] = costs[i][color] + min2
            else:
                curr[color] = costs[i][color] + min1

        prev = curr

    return min(prev)
```
