# Burst Balloons

the signature interval dp problem ( well one of the signatures atleast )
Though the problem formulation is just cancer.

## Problem

n elems, picking one gives you `nums[i - 1] * nums[i] * nums[i + 1]`, out of bounds treat as
one. Find the max you can get.

## Solution

Even if you know the idea, the impl often gets tricky for this one.

The problem with picking some k and splitting at that is the left and right could
be very different that the immediate neighbors, and in fact would depend on the state
of things prior.

```
1 2 3 4
if I pick 2, my array becomes
1 3 4
Now if I pick 3, I can only know 1 is to the left if I know the entire path taken
to get here
```

The trick is to treat the "k" we select as the LAST element to pick in any "subrange"
that we are at.

If k is the last balloon popped inside interval [i, j], then when k is popped, every other
balloon in [i, j] is gone. Therefore its neighbors are exactly i-1 and j+1.

```python
class Solution:
    def maxCoins(self, nums: list[int]) -> int:
        n = len(nums)

        def get(pos):
            return 1 if pos < 0 or pos >= n else nums[pos]

        @cache
        def f(i, j):
            if i > j:
                return 0

            ans = max(
                get(i - 1) * get(j + 1) * nums[k] + f(i, k - 1) + f(k + 1, j)
                for k in range(i, j + 1)
            )

            return ans

        return f(0, n - 1)
```
