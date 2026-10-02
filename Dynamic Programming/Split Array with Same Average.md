---
leetcode_url: https://leetcode.com/problems/split-array-with-same-average/
---

# Split Array with Same Average

Can you split an array into two non-empty halves such that average on both is same?

## Solution

Looks deceptively like subset sum EXCEPT average is a property of the length as well.

Note that if it's possible to do that average split then the deviation from mean on both
subsets is 0.
If you work on a transformed array where $b_i = a_ - a_{mean}$
Then the problem becomes, can I split into two subarrays such that the sum of both is 0.
Then note that is the sum of one is 0, the other will be 0, so all I need to do is check
if some subset exists where sum is 0.

This then becomes a trivial subset sum IFF you handle the fractional bit nicely in impl.
$b_i = a_i - \frac{S}{n}$, so we need to use scaled $b_i$s.

```python
class Solution:
    def splitArraySameAverage(self, nums: list[int]) -> bool:
        n, s = len(nums), sum(nums)
        nums = [n * x - s for x in nums]

        if n <= 1:
            return False

        # to handle the full case cleanly
        # just delete one element, whichever group it
        # belonged to would break but you will still have
        # group with 0 sum
        nums.pop()
        n = n - 1

        # can I make k using the first i elems
        # note that I still need to handle the empty case
        # a 0 is trivally made by the usual base case
        @cache
        def f(i, k):
            if i < 0:
                return False

            cur = nums[i]
            if cur == k:
                return True

            return f(i - 1, k) or f(i - 1, k - cur)

        return f(n-1, 0)
```

This got mled, I'm pretty sure I can do something to have it JUST get by but the bright
idea and why the number of elements were so low was all for MITM, which drops the sum
dimension entirely.

**that something to have it get by**
Notice that by my full case handling, I'm breaking the recursion to have to search for ONE
such 0 sum group, when two existed originally and one of those would have to be of size < len/2.

Then I must keep the full set of elems and instead extend the usual subset sum idea to also
take into account the size of the subset, making it a state. Then I can iterate over the
smaller subset's size.

```python
class Solution:
    def splitArraySameAverage(self, nums: list[int]) -> bool:
        n = len(nums)
        total = sum(nums)

        @cache
        def f(i: int, k: int, need: int) -> bool:
            if k == 0:
                # if we are picking 0 elems, only then can make the empty set
                return need == 0

            if i < 0 or i + 1 < k:
                return False

            return f(i - 1, k, need) or f(i - 1, k - 1, need - nums[i])

        # there are two subsets with same avg
        # we are looking for the smaller one
        for k in range(1, n // 2 + 1):
            if (k * total) % n != 0:
                continue

            need = (k * total) // n

            if f(n - 1, k, need):
                return True

        return False
```

> in sol 1, I wanted a fixed target regardless of length hence mean centering was needed
> in the 2nd one it wasn't as we are iterating on len so know exactly what tgt we want

### WHAT IF the sums were too large?

That is where you do the same but MITM way, problem being I can't have the sum S as state.
Figure out all sums using using both halves, then try to combine by picking a from one set
and checking if -a is there in the second one.

Notice that we NEED to keep track of sizes so that we can handle the variable target.

```python
class Solution:
    def splitArraySameAverage(self, nums: list[int]) -> bool:
        n, total = len(nums), sum(nums)
        m = n // 2

        def gen(a):
            dp = [{0}] + [set() for _ in a]
            for x in a:
                for k in range(len(a), 0, -1):
                    dp[k] |= {s + x for s in dp[k - 1]}
            return dp

        a, b = gen(nums[:m]), gen(nums[m:])

        for k in range(1, n // 2 + 1):
            if k * total % n:
                continue

            need = (k * total) // n

            for i in range(k + 1):
                if i < len(a) and k - i < len(b):
                    if any(need - x in b[k - i] for x in a[i]):
                        return True

        return False
```

With meean centering, this becomes MUCH more simple as you don't need a variable target
compute from sizes.

```python
class Solution:
    def splitArraySameAverage(self, nums: list[int]) -> bool:
        n, total = len(nums), sum(nums)
        nums = [n * x - total for x in nums]

        nums.pop()  # removes full-array case
        m = len(nums) // 2

        def gen(a):
            s = set()
            for x in a:
                s |= {x} | {y + x for y in s}
            return s

        a, b = gen(nums[:m]), gen(nums[m:])

        # subset entirely in one half
        if 0 in a or 0 in b:
            return True

        # subset using both halves
        return any(-x in b for x in a)
```
