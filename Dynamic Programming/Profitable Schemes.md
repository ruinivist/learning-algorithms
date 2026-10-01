# Profitable Schemes

n members. crimes = list of (profit i, count i members needed). Cannot reuse members.
Count subsets of crimes such that they rake in atleast minProfit.

## Solution

this looks awfully like subset sum or knapsack.
You can say that profit i = value, count i = wt.

So count of ways I can choose such that value >= V ( as opposed to max in knapsack ) and
wt <= W ( same as knapsack ).

Note that I did get another whole factor over just knapsack.

A max aggregates of values, what if I just not aggregate and instead keep each value, that's my
O(n) factor.

f(first i, v, wt) = number of ways. That doesn't look good.
let's correct, v = 100 x 100 so I that is enough by all means.

Now two are for sure, I NEED the f(...) to be a count, so I need v and wt as states.
i would be first i. Initially I missed that minProfit was just 100, so my v can be just
that, after all to account for thresholds, I only care about values below, any above
can just be clubbed together, which is what completes the solution.

> note that you can only do a push dp as you can go drom current -> "clubbed" which is
> an aggregate but not back, as the max destroys that information.
> if you change the state to "profit still needed" then the problem shifts to handle
> that clubbing so then you can technically write a pull dp.

```python
class Solution:
    def profitableSchemes(
        self, W: int, minP: int, wt: list[int], val: list[int]
    ) -> int:
        n = len(wt)
        mod = int(1e9 + 7)

        @cache
        def f(i, w, v):
            if i == n:
                return 1 if v == minP else 0

            # skip
            ans = f(i + 1, w, v)
            # take
            if w + wt[i] <= W:
                ans += f(i + 1, w + wt[i], min(minP, v + val[i]))
                ans %= mod

            return ans % mod

        return f(0, 0, 0)
```
