# Count unique BSTs

$$
\boxed{dp[n] = \sum_{root=1}^{n} dp[root-1]\cdot dp[n-root]}
$$

where $dp(n) = \text{count where you havve n ordered nodes}$
base cases are $dp[0] = 1$, $dp[1] = 1$.

You could do it in two states liek the II varition of it with `f(st,en)`, but note that ultimately the number of ways depends only on length, as long as you REPEAT those lengths, you're fine.

Think of it this way
`f(1,3)` vs `f(4,6)`, you can do a bijective map of `4...6` to be ordered as `1..3` the BST property is satisfied and in fact each tree in former would be a bijective map of each tree in later.

```python
class Solution:
    def numTrees(self, n: int) -> int:
        @cache
        def f(i):
            if i <= 1:
                return 1

            ans = 0
            # bijective map so all you care about is possible "orders"
            # a 10-15, is reduced to a 1-5
            for root in range(1, i + 1):
                # say I make root my root
                ans += f(root - 1) * f(i - root)
            return ans

        return f(n)
```
