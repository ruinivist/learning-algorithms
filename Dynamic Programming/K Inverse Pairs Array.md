# K Inverse Pairs Array

An inverse pair is just an inversion, pair being the (i,j) index pair.
For permutations of length n, count ones which have exactly k inverse pairs.

## Solution

I feel like this is another one of those that invoke permutation theory and can have
a nice solution using some property there but let's try a dp first.

I went for something f(first i taken, k inversions) but the state does not encode an order.
For example if you placed 12 or 21, if we now add 3, these cases are possible

```text
12 as base
3 12 => 2 inv
1 3 2 => 1 inv
12 3 => 0 inv

21 as base
3 21 => 2 inv
2 3 1 => 1 inv
21 3 => 0 inv

note that these are new inversions
```

Then the claim is, no matter what order you have, if you have placed i of the first smaller
ones, then you can always make upto i inversion from your new placement and each of those are
different placements to count.

The idea is that in a bag of numbers such that all are smaller than yours. If you want to
keep the inversion same, you can move to right, if you want to increase it, you can move to
left.

With this the naive impl is

```python
class Solution:
    def kInversePairs(self, n: int, k: int) -> int:
        mod = int(1e9 + 7)

        # need to place i next and am at j inversions
        @cache
        def f(i, j):
            if i == n:
                return j == k

            ans = 0
            # can create upto i inversions
            can_add = min(i, k - j)
            for inv in range(can_add + 1):
                ans += f(i + 1, j + inv)
                ans %= mod

            return ans

        return f(0, 0)
```

This TLEs, we need to eliminate the inner sum. Note that it sums over f(i+1, j...j+can_add).
We need a prefix cache on that.

You need a prefix sum optim and to that iterative is the way, but here's a nice recursive
way first, using double cache.

```python
class Solution:
    def kInversePairs(self, n: int, k: int) -> int:
        MOD = 10**9 + 7

        # prefix sum of f(i,0...j)
        @cache
        def pref(i, j):
            if j < 0:
                return 0

            return (pref(i, j - 1) + f(i, j)) % MOD

        @cache
        def f(i, j):
            if j == k:
                return 1

            if i == n:
                return 0

            hi = min(k, j + i)

            return (pref(i + 1, hi) - pref(i + 1, j - 1)) % MOD

        return f(0, 0)
```

But event this TLEs.

```python
class Solution:
    def kInversePairs(self, n: int, k: int) -> int:
        MOD = 10**9 + 7

        # dp(i) = count of prefix permutations with i inversions
        dp = [0] * (k + 1)
        dp[0] = 1

        for i in range(n):
            new = [0] * (k + 1)
            window = 0

            # with the new i, you can make 0...i more inversions
            # so prev inversions must be from k-i to k
            for j in range(k + 1):
                window += dp[j]

                if j - i - 1 >= 0:
                    window -= dp[j - i - 1]

                new[j] = window % MOD

            dp = new

        return dp[k]
```
